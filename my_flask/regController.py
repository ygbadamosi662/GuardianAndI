from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, Schema, ValidationError
from models import storage
from models.school import School
from models.guardian import Guardian
from models.student import Student
from models.guard import Guard
from models.registry import Registry
# from models.notification import Notification
from utility import util
from global_variables import SCHOOL, GUARDIAN
from repos.studentRepo import StudentRepo
from Enums.gender_enum import Gender
from Enums.tag_enum import Tag
from Enums.status_enum import Status


reg_bp = Blueprint('reg', __name__)
# ma = Marshmallow(reg_bp)


class SchoolSchema(Schema):
    school_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    address = fields.String(required=True)
    city = fields.String(required=True)

school_schema = SchoolSchema()

class GuardianSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    gender = fields.Enum(Gender)
    dob = fields.Date("iso")

guardian_schema = GuardianSchema()

class StudentSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    gender = fields.Enum(Gender)
    grade = fields.String(required=True)
    dob = fields.Date("iso")
    
student_schema = StudentSchema()

student_repo = StudentRepo()
    

@reg_bp.route('/reg/school', methods=['POST'])
def schoolReg():
    try:
        data = request.get_json()
        schoolData = school_schema.load(data)

        school = School(school_name=schoolData['school_name'], email=schoolData['email'], 
                        password=schoolData['password'], address=schoolData['address'], 
                        city=schoolData['city'])
        
        storage.new(school)
        storage.save()
        storage.close()

        return jsonify(school_schema.dump(schoolData)), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400
    
@reg_bp.route('/reg/guardian', methods=['POST'])
def guardianReg():  
    try:
        data = request.get_json()
        guardianData = guardian_schema.load(data)

        guardian = Guardian(first_name=guardianData['first_name'], last_name=guardianData['last_name'], email=guardianData['email'], password=guardianData['password'], gender=guardianData['gender'], dob=guardianData['dob'])
        
        storage.new(guardian)
        storage.save()
        storage.close()

        return jsonify(guardian_schema.dump(guardianData)), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400
    

@reg_bp.route('/reg/student', methods=['POST'])
@jwt_required()
def studentReg():
    try:
        data = request.get_json()
        studentData = student_schema.load(data)
        
        # jwt_token = request.headers.get('Authorization')[7:]
        payload = get_jwt_identity()

        student = Student(first_name=studentData['first_name'], last_name=studentData['last_name'], email=studentData['email'], gender=studentData['gender'], dob=studentData['dob'], grade=studentData['grade'])

        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()
            if school:
                student.student_school = school
                util.persistModel(student)

                registry = Registry(registry_student=student_repo.findByEmail(studentData['email']), registry_school=school, status=Status.ACTIVE)
                util.persistModel(registry)
            else:    
                return {'message': 'something is wrong, school not set'}, 400
        
        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()
            if guardian:
                util.persistModel(student)
                studentSaved = student_repo.findByEmail(studentData['email'])

                guard = Guard(guard_student=studentSaved, guard_guardian=guardian, tag=Tag.SUPER_GUARDIAN, status=Status.ACTIVE)
                util.persistModel(guard)
            else:
                return {'message': 'something is wrong, guardian not set'}, 400    
        
        storage.close()

        return jsonify(student_schema.dump(studentData)), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400