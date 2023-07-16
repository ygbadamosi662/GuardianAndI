from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from response_object import getStudentResponse, getListOfResponseObjects
from sqlalchemy.exc import SQLAlchemyError
from Enums.status_enum import Status
from global_variables import SCHOOL, STUDENT, REGISTRY
from utility import util
from repos.studentRepo import StudentRepo
from repos.registryRepo import RegistryRepo


school_bp = Blueprint('school', __name__)
student_repo = StudentRepo()
registry_repo = RegistryRepo()



@school_bp.route('/school/get/students/<grade>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def pageStudentsByGrade(grade, page):
    try:
        # checks if jwt_toke is blacklisted
        if util.validate_against_jwt_blacklist():
            return {'Message': 'Your session has expired, login again'}, 400
        
        payload = get_jwt_identity()

        # checks if user is permitted
        if payload['model'] != SCHOOL:
            return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400

        school = util.getInstanceFromJwt()
        if not school:
            return {'message': 'Error Error!'}, 400

        students = student_repo.pageBySchoolAndGrade(school, grade, page)
        
        return jsonify(getListOfResponseObjects(STUDENT, students, True)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@school_bp.route('/get/registry/history/<status>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def getGuardianGuardHistory(status, page):
    try:
        # checks if jwt_toke is blacklisted
        if util.validate_against_jwt_blacklist():
            return {'Message': 'Your session has expired, login again'}, 400
        
        payload = get_jwt_identity()
        # checks if user is permitted
        if payload['model'] != SCHOOL:
            return {'message': 'Invalid Credentials, {} is not allowed'.format(payload['model'])}, 400

        school = util.getInstanceFromJwt()
        if not school:
            return {'message': 'Error Error!'}, 400

        realStatus = {}
        if status == 'active':
            realStatus = Status.ACTIVE

        if status == 'inactive':
            realStatus = Status.INACTIVE    

        registries = registry_repo.pageBySchoolAndStatus(school, realStatus, page)
        
        return jsonify(getListOfResponseObjects(REGISTRY, registries, True)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
