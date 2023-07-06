from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from utility import util
from models import storage
from response_object import getStudentResponse, getListOfResponseObjects, getGuardResponse
from repos.studentRepo import StudentRepo
from repos.guardRepo import GuardRepo, Guard
from repos.guardianRepo import GuardianRepo
from global_variables import SCHOOL, STUDENT, GUARDIAN
from Enums.tag_enum import Tag
from Enums.status_enum import Status
from schemas import link_schema


student_bp = Blueprint('student', __name__)
student_repo = StudentRepo()
guard_repo = GuardRepo()
guardian_repo = GuardianRepo()


@student_bp.route('/student', methods=['GET'])
@jwt_required(optional=False)
def getStudent():
    email = request.args.get('email')
    student = student_repo.findByEmail(email)
    if student:
        return jsonify(getStudentResponse(student)), 200
    
    return {'error_message': 'Cant find student'}, 400



@student_bp.route('/students', methods=['GET'])
@jwt_required(optional=False)
def getStudents():
    payload = get_jwt_identity()
    if payload['model'] != SCHOOL:
        return {'message': 'Invalid Credentials'}, 400
    
    students = util.getInstanceFromJwt().school_students
    return jsonify(getListOfResponseObjects(STUDENT, students)), 200

@student_bp.route('/link', methods=['POST'])
@jwt_required(optional=False)
def linkStudent():
    try:
        data = request.get_json()
        linkData = link_schema.load(data)

        payload = get_jwt_identity()
        # check if the user is a guardian
        if payload['model'] != GUARDIAN:
            return {'message': 'Invalid Credentials'}, 400
        
        student = student_repo.findByEmail(linkData['student_email'])
        # check if student exists
        if not student:
            return {'message': 'Student does not exist'}, 400
        
        # check super-guardian limit
        if (linkData['tag'] == Tag.SUPER_GUARDIAN) and (util.superLimit(student) == False):
            return {'message': 'A student can only have two super-guardians'}, 400
        
        guardian = util.getInstanceFromJwt()
        # checki if user is a guardian, super-guardian and an active guardian to the provided student
        if util.isGuardian(student, guardian,True, True) == False:
            return {'message': 'Invalid Credentials'}, 400

        new_guardian = guardian_repo.findByEmail(linkData['guardian_email'])
        # check if new guardian exists
        if not new_guardian:
            return {'message': 'guardian does not exist'}, 400
        
        # check if new_guardian is already a guardian to the provided student
        if util.isGuardian(student, new_guardian) == True:
            return {'message': linkData['guardian_email']+' is already a guardian to '+linkData['student_email']}, 400
        
        guard = Guard(guard_student=student, guard_guardian=new_guardian, tag=linkData['tag'], status=Status.ACTIVE_PENDING)
        util.persistModel(guard)

        storage.close()

        return jsonify(getGuardResponse(guard))
    
    except ValidationError as err:
        return {'message': err.messages}, 400
    except SQLAlchemyError as err:
        return {'message': err._message()}