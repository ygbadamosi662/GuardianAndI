from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from response_object import getListOfResponseObjects, getGuardResponse
from sqlalchemy.exc import SQLAlchemyError
from global_variables import GUARD, GUARDIAN, UNLINKED
from utility import util
from Enums.status_enum import Status
from Enums.tag_enum import Tag
from Enums.permit_enum import Permit
from services.note_service import note_service
from repos.studentRepo import StudentRepo
from repos.guardRepo import GuardRepo


guardian_bp = Blueprint('guardian', __name__)
student_repo = StudentRepo()
guard_repo = GuardRepo()


@guardian_bp.route('/get/students/<tag>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def guardianGetsStudents(tag, page):
    try:
        payload = get_jwt_identity()

        if payload['model'] != GUARDIAN:
            return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400

        guardian = util.getInstanceFromJwt()
        if not guardian:
            return {'mesaage': 'ERROR ERROR!'}, 400

        realTag = {}

        if tag == 'aux':
            realTag = Tag.AUXILLARY_GUARDIAN

        if tag == 'super':
            realTag = Tag.SUPER_GUARDIAN

        guards = guard_repo.pageByGuardianAndStatusAndTag(guardian, Status.ACTIVE, realTag, page)
        
        return jsonify(getListOfResponseObjects(GUARD, guards, True)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@guardian_bp.route('/get/guards/history/<status>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def getGuardianGuardHistory(status, page):
    try:
        payload = get_jwt_identity()
        # checks if user is permitted
        if payload['model'] != GUARDIAN:
            return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400

        guardian = util.getInstanceFromJwt()
        if not guardian:
            return {'message': 'Error Error!'}, 400

        realStatus = {}
        if status == 'active':
            realStatus = Status.ACTIVE

        if status == 'inactive':
            realStatus = Status.INACTIVE    

        guards = guard_repo.pageByGuardianAndStatus(guardian, realStatus, page)
        util.closeSession()

        return jsonify(getListOfResponseObjects(GUARD, guards, True)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@guardian_bp.route('/guard/confirm/status/<string:yes_or_no>/<int:id>', methods=['GET'])
@jwt_required(optional=False)
def guard_status(id, yes_or_no):
    try:
        payload = get_jwt_identity()

        if not id:
            return {'Message': 'find what'}, 400

        if payload['model'] != GUARDIAN:
            return {'Message': 'Invalid Credentials'}, 400
        
        guard = guard_repo.findById(id)
        if not guard:
            return {'Message': 'Guard does not exist'}, 400
        
        if guard.status != Status.ACTIVE_PENDING:
            return {'Message': 'Cant perform action'}, 400
        
        guardian = util.getInstanceFromJwt()
        
        # validate guard
        if guard.guard_guardian != guardian:
            return {'Message': 'Invalid Credentials'}, 400
        
        if yes_or_no == 'yes':
            guard.status = Status.ACTIVE

        if yes_or_no == 'no':
            guard.status = Status.INACTIVE

        util.persistModel(guard)
        # notify super guardians
        guardians = util.get_student_guardians(guard.guard_student, Tag.SUPER_GUARDIAN, Status.ACTIVE)
        for g in guardians:
            for g in guardians:
                note_service.create_noti(guardian, g, guard, Permit.READONLY)

        return jsonify(getGuardResponse(guard)), 200
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@guardian_bp.route('/guard/unlink/<int:id>', methods=['GET'])
@jwt_required(optional=False)
def unlink(id):
    try:
        payload = get_jwt_identity()
        if payload['model'] != GUARDIAN:
            return {'Message': 'Invalid Credentials'}, 400
        
        guard = guard_repo.findById(id)
        if not guard:
            return {'Message': 'Guard does not exist'}, 400
        
        guardian = util.getInstanceFromJwt()
        
        if (util.student_validate_guardian(guard.guard_student, guardian, 'super') == False) and (guard.guard_guardian != guardian):
            return {'Message': 'Invalid Credentials'}, 400
        
        if guard.tag == Tag.SUPER_GUARDIAN:
            if guardian != guard.guard_guardian:
                return {'Message': 'Invalid Credentials'}, 400

        guard.status = Status.INACTIVE
        util.persistModel(guard)
        
        # notify guardians
        if (guard.tag != Tag.SUPER_GUARDIAN) and (guardian != guard.guard_guardian):
            note_service.create_noti(guardian, guard.guard_guardian, guard, Permit.READONLY, UNLINKED)
        
        for g in util.get_active_student_guardians(guard.guard_student, Tag.SUPER_GUARDIAN):
            if g != guardian:
                note_service.create_noti(guardian, g, guard, Permit.READONLY, UNLINKED)

        return jsonify(getGuardResponse(guard)), 200
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
