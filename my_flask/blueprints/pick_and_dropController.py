from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from schemas import pad_schema
from models.pick_and_drop import PickAndDrop
from response_object import getListOfResponseObjects, getPadResponse
from models import storage
from global_variables import GUARD, GUARDIAN, SCHOOL, PICK_AND_DROP, REGISTRY, STUDENT
from utility import util
from Enums.status_enum import Status
from Enums.auth_enum import Auth
from Enums.action_enum import Action
from Enums.tag_enum import Tag
from repos.guardianRepo import guardian_repo
from repos.guardRepo import guard_repo
from repos.notificationRepo import note_repo
from repos.pick_and_dropRepo import pad_repo
from repos.registryRepo import registry_repo
from repos.schoolRepo import school_repo
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

        student = student_repo.findByEmail(padData['student_email'])

        # checks if student exist
        if not student:
            return {'message': 'student does not exist'}, 400
        
        guardian = util.getInstanceFromJwt()
        
        guard = guard_repo.findByStudentAndGuardianAndStatus(student, guardian, Status.ACTIVE)
        # checks if guard valid
        if not guard:
            return {'message': 'Inavalid Credentials'}, 400
        
        # write a check if guardian has open pad
        
        registry = {}
        
        registry = registry_repo.findByStudentAndStatus(student, Status.ACTIVE)
        if not registry:
            return {'message': 'Student does not have any active registration'}
        
        if util.check_for_active_registry_pad(registry, True):
            return {'message': 'Student already in play'}, 400
        
        actor = {}
        if padData['action'] == 'pick':
            actor = Action.PICK_UP
            
        if padData['action'] == 'drop':
            actor = Action.DROP_OFF
        
        pad = PickAndDrop(PAD_registry=registry, PAD_guard= guard, action=actor, auth=Auth.initiate())
        
        util.persistModel(pad)
        util.closeSession()

        return jsonify(getPadResponse(pad)), 200
    except ValidationError as err:
        return {'message': err.messages}, 400
    
@pad_bp.route('/school/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def school_yes_or_no(id, yes_or_no):
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
    util.closeSession()

    return jsonify(getPadResponse(pad)), 200

@pad_bp.route('/guardian/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def guardian_yes_or_no(id, yes_or_no):
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
            util.closeSession()
            return jsonify(getPadResponse(pad)), 200
        
        if pad.auth_provider != guardian:
            pad.auth = pad.auth.next(False)
            util.persistModel(pad)
            util.closeSession()
            # when notification is implemented an alarm otification should be use here
            return {
                'Message': 'Conflicting AUTHORIZATION',
                'pad': jsonify(getPadResponse(pad))
                }, 400
        
    if yes_or_no == 'yes':
        if pad.auth == Auth.SG_IN:
            name = pad.auth_provider.first_name +" "+pad.auth_provider.last_name
            
            return {'message': 'We already have the required auth'+
                    ' from {}, thank you'.format(name)}, 400
            
        pad.auth = pad.auth.next(True)
        pad.auth_provider = guardian

    if yes_or_no == 'no':
        if pad.auth == Auth.SG_OUT:
            name = pad.auth_provider.first_name +" "+pad.auth_provider.last_name
            return {'message': 'We already have the required auth '+
                    'from {}, thank you'.format(name)}, 400
        pad.auth == Auth.SG_OUT
        pad.auth_provider = guardian

    util.persistModel(pad)
    util.closeSession()

    return jsonify(getPadResponse(pad)), 200

@pad_bp.route('/school/pick/ready/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def pick_up_ready(id, yes_or_no):
    payload = get_jwt_identity()
    # checks credentials
    if payload['model'] != SCHOOL:
        return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400
    
    pad = pad_repo.findById(id)
    # checks if pad exists
    if not pad:
        return {'Message': 'PAD does not exist'}, 400
    
    school = util.getInstanceFromJwt()
    
    if util.pad_validate_school(pad, school) == False:
        return {'Message': 'Invalid Credentials'}, 400
    
    # checks pad action
    if pad.action != Action.PICK_UP:
        return {'Message': 'Wrong address, this end-point serves only PICK UPS'}, 400

    # checks authorization
    if pad.auth != Auth.SG_IN:
        return {'Message': 'PAD does not have the proper Authorization'}, 400
    
    # READY if yes
    if yes_or_no == 'yes':
        pad.auth = pad.auth.nextOfSG_IN(True)

    # CONFLICT if no
    if yes_or_no == 'no':
        pad.auth = pad.auth.nextOfSG_IN(False)

    util.persistModel(pad)
    util.closeSession()

    return jsonify(getPadResponse(pad)), 200

@pad_bp.route('/guardian/drop/ready/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def drop_off_ready(id, yes_or_no):
    payload = get_jwt_identity()
    # checks credentials
    if payload['model'] != GUARDIAN:
        print(payload['model'])
        return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400
    
    pad = pad_repo.findById(id)
    # checks if pad exists
    if not pad:
        return {'Message': 'PAD does not exist'}, 400
    
    guardian = util.getInstanceFromJwt()

    # checks credentials
    if guardian != pad.PAD_guard.guard_guardian:
        return {'Message': 'Inavalid Credentials'}, 400

    # checks the guard validation
    if util.validateGuard(pad.PAD_guard) == False:
        return {'Message': 'Guard have been revoked'}, 400
    
    # checks pad action
    if pad.action != Action.DROP_OFF:
        return {'Message': 'Wrong address, this end-point serves only DROP OFFs'}, 400

    # checks authorization
    if pad.auth != Auth.SG_IN:
        return {'Message': 'PAD does not have the proper Authorization'}, 400
    
    # READY if yes
    if yes_or_no == 'yes':
        pad.auth = pad.auth.nextOfSG_IN(True)

    # CONFLICT if no
    if yes_or_no == 'no':
        pad.auth = pad.auth.nextOfSG_IN(False)
   
    util.persistModel(pad)
    util.closeSession()

    return jsonify(getPadResponse(pad)), 200

@pad_bp.route('/shoo/<int:id>/<string:yes_or_no>', methods=['GET'])
@jwt_required(optional=False)
def shoo(id, yes_or_no):
    payload = get_jwt_identity()
    user = {}
    to = {}
    pad = pad_repo.findById(id)
    # checks if pad exist
    if not pad:
        return {'Message': 'PAD does not exist'}, 400
    
    
    if payload['model'] == GUARDIAN:
        guardian = util.getInstanceFromJwt()
        # checks guardian validity
        if util.pad_validate_guardian(pad, guardian) == False:
            return {'Message': 'Invalid Credentials'}, 400
        
        # checks super_guardian validity
        if util.pad_validate_guardian(pad, guardian, 'super') == False:
            return {'Message': 'Above Your pay grade'}, 400
        
        if pad.auth == Auth.READY:
            msg = 'Guardian {} is READY, but is not in possesion of your ward yet'
            guardian_name = guardian.first_name +" "+ guardian.last_name
            return {'Message': msg.format(guardian_name)}, 400
        
        
        # checks if action is permitted
        if pad.action != Action.PICK_UP:
            return {'Message': 'Invalid Credentials'}, 400
        
        if pad.auth == Auth.READY:
            msg = 'Guardian {} is READY, but is not in possesion of your ward {} yet'
            guardian_name = guardian
            return {'Message': msg.format()}
        
        user = guardian
        
    if payload['model'] == SCHOOL:
        
        school = util.getInstanceFromJwt()
        # checks school validity
        if util.pad_validate_school(pad, school) == False:
            return {'Message': 'Invalid Credentials'}, 400
        
        if pad.auth == Auth.READY:
            msg = 'Guardian {} is READY, but is not in possesion of your student yet'
            guardian_name = guardian.first_name +" "+ guardian.last_name
            return {'Message': msg.format(guardian_name)}, 400
        
        # checks if action is permitted
        if pad.action != Action.DROP_OFF:
            return {'Message': 'Invalid Credentials'}, 400
        
        user = school

    if pad.auth == Auth.CONFLICT:
            return {'Message': 'There is a CONFLICT with the given PAD'}, 400
            
    
    # checks authorization
    if (pad.auth != Auth.IN_TRANSIT) and (pad.auth != Auth.ARRIVED):
        return {'Message': 'PAD is not READY'}, 400
    
    # if ARRIVED
    if pad.auth == Auth.ARRIVED:
        return {'Message': 'Student has ARRIVED already'}, 200
    
    if yes_or_no == 'no':
        pad.auth = pad.auth.next(False)
        # raise an alarm

    if yes_or_no == 'yes':
        pad.auth = pad.auth.next(True)

    util.persistModel(pad)
    util.closeSession()

    return jsonify(getPadResponse(pad)), 200

@pad_bp.route('/pad/<int:id>', methods=['GET'])
@jwt_required(optional=False)
def get_pad(id: int):
    payload = get_jwt_identity()
    if not id:
        return {'Message': 'Which pad?...id is not set'}, 400

    pad = pad_repo.findById(id)
    if not pad:
        return {'Message': 'PAD does not exist'}, 400
    
    if payload['model'] == GUARDIAN:
        guardian = util.getInstanceFromJwt()
        
        # check tag
        if util.pad_validate_guardian(pad, guardian, 'all'):
            return {'Message': 'Invalid Credentials'}, 400
            
        if util.pad_validate_guardian(pad, guardian, 'school') or util.pad_validate_guardian(pad, guardian, 'aux'):
            if pad.PAD_guard.guard_guardian != guardian:
                return {'Message': 'Invalid Credentials'}, 400

    if payload['model'] == SCHOOL:
        school = util.getInstanceFromJwt()

        # validate school
        if util.pad_validate_school(pad, school) == False:
            return {'Message': 'Invalid Credentials'}, 400
        
    util.closeSession()

    return jsonify(getPadResponse(pad)), 200

@pad_bp.route('/pads/<string:filter>/', defaults={'page': 1, 'action': 'all'}, methods=['GET'])
@pad_bp.route('/pads/<string:filter>/<int:page>/', defaults={'action': 'all'}, methods=['GET'])
@pad_bp.route('/pads/<string:filter>/<int:page>/<string:action>', methods=['GET'])
@jwt_required(optional=False)
def get_pads(filter, page, action):
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
                print(pads)
            
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

    util.closeSession()
    
    return jsonify(getListOfResponseObjects(PICK_AND_DROP, pads)), 200