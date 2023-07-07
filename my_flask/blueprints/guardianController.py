from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from response_object import getListOfResponseObjects
from models import storage
from global_variables import GUARD, GUARDIAN
from utility import util
from Enums.status_enum import Status
from Enums.tag_enum import Tag
from repos.studentRepo import StudentRepo
from repos.guardRepo import GuardRepo


guardian_bp = Blueprint('guardian', __name__)
student_repo = StudentRepo()
guard_repo = GuardRepo()


@guardian_bp.route('/get/students/<tag>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def guardianGetsStudents(tag, page):
    payload = get_jwt_identity()

    if payload['model'] != GUARDIAN:
        return {'message': 'Invalid Credentials'}, 400
    
    guardian = util.getInstanceFromJwt()
    if not guardian:
        return {'mesaage': 'ERROR ERROR!'}, 400
    
    realTag = {}

    if tag == 'aux':
        realTag = Tag.AUXILLARY_GUARDIAN

    if tag == 'super':
        realTag = Tag.SUPER_GUARDIAN

    guards = guard_repo.pageByGuardianAndStatusAndTag(guardian, Status.ACTIVE, realTag, page)
    util.closeSession()

    return jsonify(getListOfResponseObjects(GUARD, guards, True)), 200

@guardian_bp.route('/get/guards/history/<status>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def getGuardianGuardHistory(status, page):
    payload = get_jwt_identity()
    # checks if user is permitted
    if payload['model'] != GUARDIAN:
        return {'message': 'Invalid Credentials'}, 400
    
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

