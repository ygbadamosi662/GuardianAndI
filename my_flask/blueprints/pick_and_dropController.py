from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services.note_service import note_service
from schemas import pad_schema
from schemas import student_pad_schema
from models.pick_and_drop import PickAndDrop
from response_object import getListOfResponseObjects, getPadResponse
from global_variables import GUARDIAN, SCHOOL, PICK_AND_DROP, STUDENT, AUTHORIZATION, CONFIRMATION, CONFLICT
from utility import util
from Enums.status_enum import Status
from Enums.auth_enum import Auth
from Enums.action_enum import Action
from Enums.tag_enum import Tag
from Enums.activity_enum import Activity
from Enums.permit_enum import Permit
from repos.guardRepo import guard_repo
from repos.notificationRepo import note_repo
from repos.pick_and_dropRepo import pad_repo
from repos.registryRepo import registry_repo
from repos.studentRepo import student_repo


pad_bp = Blueprint('pad', __name__)


@pad_bp.route('/initiate', methods=['POST'])
@jwt_required(optional=False)
def initiateDrop():
    payload = get_jwt_identity()
    # checks credentials
    if payload['model'] != GUARDIAN:
        return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400
    
    try:
        data = request.get_json()
        padData = pad_schema.load(data)

        # checks if student exist
        if util.validate_table_integrity(padData['student_email'], STUDENT) == False:
            return {'message': 'student does not exist'}, 400
        
        student = student_repo.findByEmail(padData['student_email'])

        guardian = util.getInstanceFromJwt()
        
        guard = guard_repo.findByStudentAndGuardianAndStatus(student, guardian, Status.ACTIVE)
        # checks if guard valid
        if not guard:
            return {'message': 'Inavalid Credentials'}, 400
        
        # write a check if guardian has open pad
        
        registry = {}
        
        # this checks if student have an active registration
        registry = registry_repo.findByStudentAndStatus(student, Status.ACTIVE)
        if not registry:
            return {'message': 'Student does not have any active registration'}
        
        # this checks if student as any ongoing pad
        if util.check_for_active_registry_pad(registry, True):
            return {'message': 'Student already in play'}, 400
        
        act = {}
        if padData['action'] == 'pick':
            act = Action.PICK_UP
            
        if padData['action'] == 'drop':
            act = Action.DROP_OFF
        
        pad = PickAndDrop(PAD_registry=registry, PAD_guard= guard, action=act, auth=Auth.initiate())
        
        util.persistModel(pad)
        saved_pad = pad_repo.findOngoingPadByGuard(guard)

        # notify school
        note_service.create_noti(guardian, registry.registry_school, saved_pad, Permit.READ_AND_WRITE, AUTHORIZATION)

        # notify super guardians
        sups = util.get_student_guardians(student, Tag.SUPER_GUARDIAN, Status.ACTIVE)
        for sup in sups:
            if sup != guardian:
                note_service.create_noti(guardian, sup, saved_pad, Permit.READONLY)
        
        return jsonify(getPadResponse(saved_pad)), 200
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
    
@pad_bp.route('/school/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def school_yes_or_no(id, yes_or_no):
    try:
        payload = get_jwt_identity()
        if payload['model'] != SCHOOL:
            return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400

        pad = pad_repo.findById(id)
        # checks if pad exist
        if not pad:
            return {'message': 'Pick or Drop does not exist'}, 400

        school = util.getInstanceFromJwt()

        # validates school
        if util.pad_validate_school(pad, school) == False:
            return {'message': 'Invalid Credentials'}, 400

        # validates access
        if (pad.auth != Auth.INITIATED) and (pad.auth != Auth.SCHOOL_IN):
            return {'Message': 'PAD does not have the proper authorization'}, 400

        if (yes_or_no == 'yes') and (pad.auth == Auth.SCHOOL_IN):
            return {'message': 'Yes we know'}, 200

        # if school is in
        if yes_or_no == 'yes':
                pad.auth = pad.auth.next(True)

        # if school is out
        if yes_or_no == 'no':
            if pad.auth != Auth.SCHOOL_IN:
                pad.auth = pad.auth.next(False)

            if pad.auth == Auth.SCHOOL_IN:
                pad.auth = Auth.SCHOOL_OUT


        util.persistModel(pad)

        # notify the guardians accordinly
        guardians = util.get_pad_guardians(pad)
        for g in guardians:
            if pad.auth == Auth.SCHOOL_IN:
                if util.student_validate_guardian(pad.PAD_guard.guard_student, g, 'super'):
                    note_service.create_noti(school, g, pad, Permit.READ_AND_WRITE, AUTHORIZATION)

                if util.student_validate_guardian(pad.PAD_guard.guard_student, g, 'auxs'):
                    note_service.create_noti(school, g, pad, Permit.READONLY)

            if pad.auth == Auth.SCHOOL_OUT:
                note_service.create_noti(school, g, pad, Permit.READONLY)
        
        return jsonify(getPadResponse(pad)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/guardian/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def guardian_yes_or_no(id, yes_or_no):
    try:
        payload = get_jwt_identity()
        if payload['model'] != GUARDIAN:
            return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400

        pad = pad_repo.findById(id)
        # checks if pad exist
        if not pad:
            return {'message': 'Pick or Drop does not exist'}, 400

        guardian = util.getInstanceFromJwt()

        # validates guardian
        if util.pad_validate_guardian(pad, guardian, 'super') == False:
            return {'message': 'Invalid Credentials'}, 400

        # validates Auth
        if (pad.auth != Auth.SCHOOL_IN) and (pad.auth != Auth.SG_IN) and (pad.auth != Auth.SG_OUT):
            return {'Message': 'PAD does not have the proper authorization'}, 400


        # checks for conflicting Authorization
        if (yes_or_no == 'no') and (pad.auth == Auth.SG_IN):
            if pad.auth_provider == guardian:
                pad.auth = Auth.SG_OUT
                util.persistModel(pad)
                
                return jsonify(getPadResponse(pad)), 200

            if pad.auth_provider != guardian:
                # pad.auth = pad.auth.next(False)
                # util.persistModel(pad)
                
                # when notification is implemented an alarm otification should be use here
                return {
                    'Message': 'We already have the required authorization',
                    'pad': jsonify(getPadResponse(pad))
                    }, 400

        if yes_or_no == 'yes':
            if (pad.auth == Auth.SG_IN) or (pad.auth == Auth.SG_OUT):
                if pad.auth_provider == guardian:
                    if pad.auth == Auth.SG_IN:
                        name = pad.auth_provider.first_name +" "+pad.auth_provider.last_name
                        return {'message': 'We already have the required authorization'+
                        ' from {}, thank you'.format(name)}, 400
                    
                    if pad.auth == Auth.SG_OUT:
                        pad.auth = Auth.SG_IN

                if pad.auth_provider != guardian:
                    name = pad.auth_provider.first_name +" "+pad.auth_provider.last_name

                    return {'message': 'We already have the required authorization'+
                        ' from {}, thank you'.format(name)}, 400
            
            if pad.auth == Auth.SCHOOL_IN:
                pad.auth = pad.auth.next(True)
                pad.auth_provider = guardian

        if yes_or_no == 'no':
            if (pad.auth == Auth.SG_OUT) or (pad.auth == Auth.SG_IN):
                if pad.auth_provider == guardian:
                    if pad.auth == Auth.SG_OUT:
                        return {'message': 'We already have the required authorization'+
                        ' from {}, thank you'.format(name)}, 400
                    
                    if pad.auth == Auth.SG_IN:
                        pad.auth = Auth.SG_OUT

                if pad.auth_provider != guardian:
                    name = pad.auth_provider.first_name +" "+pad.auth_provider.last_name
                    return {'message': 'We already have the required authorization '+
                            'from {}, thank you'.format(name)}, 400
            
            if pad.auth == Auth.SCHOOL_IN:
                pad.auth == Auth.SG_OUT
                pad.auth_provider = guardian

        util.persistModel(pad)

        # notify guardianss
        guardians = util.get_pad_guardians(pad)
        for g in guardians:
            if util.pad_validate_guardian(pad, g, 'auxs'):
                note_service.create_noti(guardian, g, pad, Permit.READ_AND_WRITE, CONFIRMATION)

            if (util.pad_validate_guardian(pad, g, 'super')) and (g != guardian):
                note_service.create_noti(guardian, g, pad, Permit.READONLY)

        # notify school
        note_service.create_noti(guardian, util.get_pad_student_or_school(pad, SCHOOL), pad, Permit.READONLY)

        return jsonify(getPadResponse(pad)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/user/ready/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def ready(id, yes_or_no):
    try:
        pad = pad_repo.findById(id)
        # checks if pad exists
        if not pad:
            return {'Message': 'PAD does not exist'}, 400
        
        if pad.auth != Auth.SG_IN:
            return {'Message': 'Invalid Authorization'}, 400
        
        payload = get_jwt_identity()
        
        if pad.action == Action.PICK_UP:
            # checks credentials
            if payload['model'] != SCHOOL:
                return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400
            
            school = util.getInstanceFromJwt()

            if util.pad_validate_school(pad, school) == False:
                return {'Message': 'Invalid Credentials'}, 400

            # READY if yes
            if yes_or_no == 'yes':
                pad.auth = pad.auth.nextOfSG_IN(True)

            # CONFLICT if no
            if yes_or_no == 'no':
                pad.auth = pad.auth.nextOfSG_IN(False)

            # notify guardians
            guardians = util.get_pad_guardians(pad)
            for g in guardians:
                if pad.auth != Auth.CONFLICT:
                    note_service.create_noti(school, g, pad, Permit.READONLY)
                if pad.auth == Auth.CONFLICT:
                    note_service.create_noti(school, g, pad, Permit.READONLY, CONFLICT)
        
        if pad.action == Action.DROP_OFF:
            # checks credentials
            if payload['model'] != GUARDIAN:
                return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400
            
            guardian = util.getInstanceFromJwt()

            if util.pad_validate_guardian(pad, guardian, 'super') == False:
                return {'Message': 'Invalid Credentials'}, 400
            
            
            # READY if yes
            if yes_or_no == 'yes':
                pad.auth = pad.auth.nextOfSG_IN(True)

            # CONFLICT if no
            if yes_or_no == 'no':
                pad.auth = pad.auth.nextOfSG_IN(False)

            # notify school
            school = util.get_pad_student_or_school(pad, SCHOOL)
            if school:
                if pad.auth != Auth.CONFLICT:
                    note_service.create_noti(guardian, school, pad, Permit.READONLY)
                if pad.auth == Auth.CONFLICT:
                    note_service.create_noti(guardian, school, pad, Permit.READONLY, CONFLICT)

            # notify guardians
            guardians = util.get_pad_guardians(pad)
            for g in guardians:
                if g != guardian:
                    if pad.auth != Auth.CONFLICT:
                        note_service.create_noti(guardian, g, pad, Permit.READONLY)
                    if pad.auth == Auth.CONFLICT:
                        note_service.create_noti(guardian, g, pad, Permit.READONLY, CONFLICT)

        util.persistModel(pad)
        
        return jsonify(getPadResponse(pad)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/shoo/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def shoo(id, yes_or_no):
    try:
        payload = get_jwt_identity()
        pad = pad_repo.findById(id)
        # checks if pad exist

        if not pad:
            return {'Message': 'PAD does not exist'}, 400
        
        if pad.auth != Auth.READY:
            return {'Message': 'Invalid Authorization'}, 400
        
        if pad.action == Action.PICK_UP:
            if payload['model'] != SCHOOL:
                return {'Message': 'Invalid Credentials'}, 400
            
            school = util.getInstanceFromJwt()
            # checks school validity
            if util.pad_validate_school(pad, school) == False:
                return {'Message': 'Invalid Credentials'}, 400
            
            if yes_or_no == 'no':
                pad.auth = pad.auth.next(False)

            if yes_or_no == 'yes':
                pad.auth = pad.auth.next(True)

            # notify guardians
            guardians = util.get_pad_guardians(pad)
            for g in guardians:
                if util.pad_validate_guardian(pad, g, 'super'):
                    if pad.auth == Auth.CONFLICT:
                        note_service.create_noti(school, g, pad, Permit.READONLY, CONFLICT)
                    if pad.auth != Auth.CONFLICT:
                        note_service.create_noti(school, g, pad, Permit.READ_AND_WRITE, CONFIRMATION)

                if util.pad_validate_guardian(pad, g, 'auxs'):
                    if pad.auth == Auth.CONFLICT:
                        note_service.create_noti(school, g, pad, Permit.READONLY, CONFLICT)
                    if pad.auth != Auth.CONFLICT:
                        note_service.create_noti(school, g, pad, Permit.READONLY)

        
        if pad.action == Action.DROP_OFF:
            if payload['model'] != GUARDIAN:
                return {'Message': 'Invalid Credentials'}, 400
            
            guardian = util.getInstanceFromJwt()
            # checks guardian validity
            if util.pad_validate_guardian(pad, guardian) == False:
                return {'Message': 'Invalid Credentials'}, 400

            # checks super_guardian validity
            if util.pad_validate_guardian(pad, guardian, 'super') == False:
                return {'Message': 'Above Your pay grade'}, 400
            
            if yes_or_no == 'no':
                pad.auth = pad.auth.next(False)

            if yes_or_no == 'yes':
                pad.auth = pad.auth.next(True)

            # notify guardians
            guardians = util.get_pad_guardians(pad)
            for g in guardians:
                if g != guardian:
                    if pad.auth == Auth.CONFLICT:
                        note_service.create_noti(guardian, g, pad, Permit.READONLY, CONFLICT)
                    if pad.auth != Auth.CONFLICT:
                        note_service.create_noti(guardian, g, pad, Permit.READONLY)

            # notify school
            school = util.get_pad_student_or_school(pad, SCHOOL)
            if school:
                note_service.create_noti(guardian, school, pad, Permit.READ_AND_WRITE, CONFIRMATION)
                
        util.persistModel(pad)

        return jsonify(getPadResponse(pad)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/arrived/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def arrived_or_not(id, yes_or_no):
    try:
        payload = get_jwt_identity()
        pad = pad_repo.findById(id)
        # checks if pad exist
        if not pad:
            return {'Message': 'PAD does not exist'}, 400
        
        if pad.auth != Auth.IN_TRANSIT:
            return {'Message': 'Invalid Authorization'}, 400
        
        if pad.action == Action.DROP_OFF:
            if payload['model'] != SCHOOL:
                return {'Message': 'Invalid Credentials'}, 400
            
            school = util.getInstanceFromJwt()
            # checks school validity
            if util.pad_validate_school(pad, school) == False:
                return {'Message': 'Invalid Credentials'}, 400
            
            if yes_or_no == 'no':
                pad.auth = pad.auth.next(False)
                
            if yes_or_no == 'yes':
                pad.auth = pad.auth.next(True)

            # notify guardians
            guardians = util.get_pad_guardians(pad)
            for g in guardians:
                if pad.auth == Auth.CONFLICT:
                    note_service.create_noti(school, g, pad, Permit.READONLY, CONFLICT)
                if pad.auth != Auth.CONFLICT:
                    note_service.create_noti(school, g, pad, Permit.READONLY)


        
        if pad.action == Action.PICK_UP:
            if payload['model'] != GUARDIAN:
                return {'Message': 'Invalid Credentials'}, 400
            
            guardian = util.getInstanceFromJwt()
            # checks guardian validity
            if util.pad_validate_guardian(pad, guardian) == False:
                return {'Message': 'Invalid Credentials'}, 400

            # checks super_guardian validity
            if util.pad_validate_guardian(pad, guardian, 'super') == False:
                return {'Message': 'Above Your pay grade'}, 400
            
            if yes_or_no == 'no':
                pad.auth = pad.auth.next(False)

            if yes_or_no == 'yes':
                pad.auth = pad.auth.next(True)

            # notify guardians
            guardians = util.get_pad_guardians(pad)
            for g in guardians:
                if g != guardian:
                    if pad.auth == Auth.CONFLICT:
                        note_service.create_noti(guardian, g, pad, Permit.READONLY, CONFLICT)
                    if pad.auth != Auth.CONFLICT:
                        note_service.create_noti(guardian, g, pad, Permit.READONLY)

            # notify school
            school = util.get_pad_student_or_school(pad, SCHOOL)
            if school:
                note_service.create_noti(guardian, school, pad, Permit.READONLY)
                
        util.persistModel(pad)

        return jsonify(getPadResponse(pad)), 200

    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/pad/<int:id>', methods=['GET'])
@jwt_required(optional=False)
def get_pad(id: int):
    try:
        payload = get_jwt_identity()
        if not id:
            return {'Message': 'Which pad?...id is not set'}, 400

        pad = pad_repo.findById(id)
        if not pad:
            return {'Message': 'PAD does not exist'}, 400

        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()

            # check tag
            if util.pad_validate_guardian(pad, guardian, 'all') == False:
                return {'Message': 'Invalid Credentials'}, 400

            if util.pad_validate_guardian(pad, guardian, 'school') or util.pad_validate_guardian(pad, guardian, 'aux'):
                if pad.PAD_guard.guard_guardian != guardian:
                    return {'Message': 'Invalid Credentials'}, 400

        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()

            # validate school
            if util.pad_validate_school(pad, school) == False:
                return {'Message': 'Invalid Credentials'}, 400
            
        return jsonify(getPadResponse(pad)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/pads/<string:filter>/', defaults={'page': 1, 'action': 'all'}, methods=['GET'])
@pad_bp.route('/pads/<string:filter>/<int:page>/', defaults={'action': 'all'}, methods=['GET'])
@pad_bp.route('/pads/<string:filter>/<int:page>/<string:action>', methods=['GET'])
@jwt_required(optional=False)
def get_pads(filter, page, action):
    try:
        payload = get_jwt_identity()

        # if guardian
        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()

            if action == 'all':
                if filter == 'all':
                    pads = pad_repo.pageByGuardian(guardian, page)

                if filter == 'unsresolved':
                    pads = pad_repo.pageUnresolvedPadByGuardian(guardian, page)

                if filter == 'resolved':
                    pads = pad_repo.pageByGuardianAndAuth(guardian, Auth.ARRIVED, page)

                if filter == 'ongoing':
                    pads = pad_repo.pageOngoingPadByGuardian(guardian, page)

                if (filter != 'all') and (filter != 'unsresolved') and (filter != 'resolved') and (filter != 'ongoing'):
                    pads = pad_repo.pageByGuardianAndAuth(guardian, util.take_string_give_authEnum(filter), page)

            if (action == 'drop') or (action == 'pick'):
                app_action = util.take_string_give_actionEnum(action)

                if filter == 'all':
                    pads = pad_repo.pageByGuardianAndAction(guardian, app_action, page)

                if filter == 'unsresolved':
                    pads = pad_repo.pageUnresolvedPadByGuardianAndAction(guardian, app_action, page)

                if filter == 'resolved':
                    pads = pad_repo.pageByGuardianAndAuthAndAction(guardian, Auth.ARRIVED, app_action, page)

                if filter == 'ongoing':
                    pads = pad_repo.pageOngoingPadByGuardianAndAction(guardian, app_action, page)

                if (filter != 'all') and (filter != 'unsresolved') and (filter != 'resolved') and (filter != 'ongoing'):
                    pads = pad_repo.pageByGuardianAndAuthAndAction(guardian, util.take_string_give_authEnum(filter), app_action, page)


        # if school
        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()

            if action == 'all':
                if filter == 'all':
                    pads = pad_repo.pageBySchool(school, page)

                if filter == 'unsresolved':
                    pads = pad_repo.pageUnresolvedPadBySchool(school, page)

                if filter == 'resolved':
                    pads = pad_repo.pageBySchoolAndAuth(school, Auth.ARRIVED, page)

                if filter == 'ongoing':
                    pads = pad_repo.pageOngoingPadBySchool(school, page)

                if (filter != 'all') and (filter != 'unsresolved') and (filter != 'resolved') and (filter != 'ongoing'):
                    app_auth = util.take_string_give_authEnum(filter)
                    if not app_auth:
                        return {'Message': 'no filter set'}, 400
                    pads = pad_repo.pageBySchoolAndAuth(school, app_auth, page)

            if (action == 'drop') or (action == 'pick'):
                app_action = util.take_string_give_actionEnum(action)

                if filter == 'all':
                    pads = pad_repo.pageBySchoolAndAction(school, app_action, page)

                if filter == 'unsresolved':
                    pads = pad_repo.pageUnresolvedPadBySchoolAndAction(school, app_action, page)

                if filter == 'resolved':
                    pads = pad_repo.pageBySchoolAndAuthAndAction(school, Auth.ARRIVED, app_action, page)

                if filter == 'ongoing':
                    pads = pad_repo.pageOngoingPadBySchoolAndAction(school, app_action, page)

                if (filter != 'all') and (filter != 'unsresolved') and (filter != 'resolved') and (filter != 'ongoing'):
                    app_auth = util.take_string_give_authEnum(filter)
                    if not app_auth:
                        return {'Message': 'no filter set'}, 400
                    pads = pad_repo.pageByGuardianAndAuthAndAction(school, app_auth, app_action, page)

        return jsonify(getListOfResponseObjects(PICK_AND_DROP, pads)), 200
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@pad_bp.route('/pads/student/', methods=['POST'])
@jwt_required(optional=False)
def studentPad():
    try:
        data = request.get_json()
        validData = student_pad_schema.load(data)

        if util.validate_table_integrity(validData['student_email'], STUDENT) == False:
            return {'Message': 'Student does not exist'}, 400
        
        student = student_repo.findByEmail(validData['student_email'])

        payload = get_jwt_identity()
        app_auth = util.take_string_give_authEnum(validData['filter'])
        app_act = util.take_string_give_actionEnum(validData['action'])

        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()
            guard = guard_repo.findByStudentAndGuardian(student, guardian)

            # checks guard
            if not guard:
                return {'Message': 'Invalid Credentials'}, 400
            
            if guard.tag != Tag.SUPER_GUARDIAN:
                if validData['filter'] == 'all':
                    if validData['action'] == 'all':
                        pads = pad_repo.pageByGuard(guard, validData['page'])

                    if app_act:
                        pads = pad_repo.pageByGuardAndAction(guard, app_act, validData['page'])

                if validData['filter'] == 'unsresolved':
                    if validData['action'] == 'all':
                        pads = pad_repo.pageUnresolvedPadByGuard(guard, validData['page'])

                    if app_act:
                        pads = pad_repo.pageUnresolvedPadByGuardAndAction(guard, app_act, validData['page'])

                if validData['filter'] == 'ongoing':
                    return jsonify(getPadResponse(pad_repo.findOngoingPadByGuard(guard))), 200
                
                # takes care of every Auth value
                if (validData['filter'] != 'all') and (validData['filter'] != 'unsresolved') and (validData['filter'] != 'ongoing'):
                    if not app_auth:
                        return {'Message': 'No filter'}, 400
                    
                    if validData['action'] == 'all':
                        pads = pad_repo.pageByGuardAndAuth(guard, app_auth, validData['page'])

                    if app_act:
                        pads = pad_repo.pageByGuardAndAuthAndAction(guard, app_auth, app_act, validData['page'])

                return jsonify(getListOfResponseObjects(PICK_AND_DROP, pads)), 200
                
            # checks super guardians status
            if guard.status != Status.ACTIVE and guard.tag != Tag.SUPER_GUARDIAN:
                return {'Message': 'Invalid Credentials'}, 400
            
            if validData['filter'] == 'all':
                if validData['action'] == 'all':
                    pads = pad_repo.pageByStudent(student, validData['page'])

                if app_act:
                    pads = pad_repo.pageByStudentAndAction(student, app_act, validData['page'])

            if validData['filter'] == 'unsresolved':
                if validData['action'] == 'all':
                    pads = pad_repo.pageUnresolvedPadByStudent(student, validData['page'])

                if app_act:
                    pads = pad_repo.pageUnresolvedPadByStudentAndAction(student, app_act, validData['page'])
                    
            if validData['filter'] == 'ongoing':
                return jsonify(getPadResponse(pad_repo.findOngoingPadByStudent(student))), 200
                
                # takes care of every Auth value
            if (validData['filter'] != 'all') and (validData['filter'] != 'unsresolved') and (validData['filter'] != 'ongoing'):
                if not app_auth:
                    return {'Message': 'No filter'}, 400
                
                if validData['action'] == 'all':
                    pads = pad_repo.pageByStudentAndAuth(student, app_auth, validData['page'])

                if app_act:
                    pads = pad_repo.pageByStudentAndAuthAndAction(student, app_auth, app_act, validData['page'])

            return jsonify(getListOfResponseObjects(PICK_AND_DROP, pads)), 200
        
        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()
            registry = registry_repo.findByStudentAndSchool(student, school)
            # checks registry
            if not registry:
                return {'Message', 'Invalid Credentials'}, 400
            
            if validData['filter'] == 'all':
                if validData['action'] == 'all':
                    pads = pad_repo.pageByRegistry(registry, validData['page'])
                if app_act:
                    pads = pad_repo.pageByRegistryAndAction(registry, app_act, validData['page'])
            if validData['filter'] == 'unsresolved':
                if validData['action'] == 'all':
                    pads = pad_repo.pageUnresolvedPadByRegistry(registry, validData['page'])
                if app_act:
                    pads = pad_repo.pageUnresolvedPadByRegistryAndAction(registry, app_act, validData['page'])
            if validData['filter'] == 'ongoing':
                return jsonify(getPadResponse(pad_repo.findOngoingPadByRegistry(registry))), 200
            
            # takes care of every Auth value
            if (validData['filter'] != 'all') and (validData['filter'] != 'unsresolved') and (validData['filter'] != 'ongoing'):
                if not app_auth:
                    return {'Message': 'No filter'}, 400
                
                if validData['action'] == 'all':
                    pads = pad_repo.pageByRegistryAndAuth(registry, app_auth, validData['page'])
                if app_act:
                    pads = pad_repo.pageByRegistryAndAuthAndAction(registry, app_auth, app_act, validData['page'])

            return jsonify(getListOfResponseObjects(PICK_AND_DROP, pads)), 200 
            

    except ValidationError as err:
        return {'Validation Error': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
