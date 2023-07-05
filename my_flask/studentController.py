from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, Schema
from utility import util
from response_object import getStudentResponse, getListOfResponseObjects
from repos.studentRepo import StudentRepo
from global_variables import SCHOOL, STUDENT


student_bp = Blueprint('student', __name__)


class EmailSchema(Schema):
    email = fields.Email(required=True)

email_schema = EmailSchema()
student_repo = StudentRepo()


@student_bp.route('/student', methods=['GET'])
@jwt_required(optional=False)
def getStudent():
    email = request.args.get('email')
    student = student_repo.findByEmail(email)
    if student:
        return jsonify(getStudentResponse(student)), 200
    
    return {'error_message': 'Cant find student'}, 400



@student_bp.route('/students', methods=['POST'])
@jwt_required(optional=False)
def getStudents():
    payload = get_jwt_identity()
    if payload['model'] != SCHOOL:
        return {'message': 'Invalid Credentials'}, 400
    
    students = util.getInstanceFromJwt().school_students

    return jsonify(getListOfResponseObjects(STUDENT, students)), 200