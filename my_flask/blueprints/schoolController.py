from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from response_object import getStudentResponse, getListOfResponseObjects
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
    payload = get_jwt_identity()

    # checks if user is permitted
    if payload['model'] != SCHOOL:
        return {'message': 'Invalid Credentials'}, 400
    
    school = util.getInstanceFromJwt()
    if not school:
        return {'message': 'Error Error!'}, 400
    
    students = student_repo.pageBySchoolAndGrade(school, grade, page)
    util.closeSession()

    return jsonify(getListOfResponseObjects(STUDENT, students, True)), 200

@school_bp.route('/get/registry/history/<status>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def getGuardianGuardHistory(status, page):
    payload = get_jwt_identity()
    # checks if user is permitted
    if payload['model'] != SCHOOL:
        return {'message': 'Invalid Credentials'}, 400
    
    school = util.getInstanceFromJwt()
    if not school:
        return {'message': 'Error Error!'}, 400
    
    realStatus = {}
    if status == 'active':
        realStatus = Status.ACTIVE

    if status == 'inactive':
        realStatus = Status.INACTIVE    
    
    registries = registry_repo.pageBySchoolAndStatus(school, realStatus, page)
    util.closeSession()

    return jsonify(getListOfResponseObjects(REGISTRY, registries, True)), 200