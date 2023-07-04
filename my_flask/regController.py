from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import fields, Schema, ValidationError
from models import storage
from models.school import School
from models.guardian import Guardian
from models.student import Student
# from models.notification import Notification
from utility import util
from global_variables import SCHOOL
from Enums import gender_enum


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
    gender = fields.Enum(gender_enum.Gender)
    dob = fields.Date("iso")

guardian_schema = GuardianSchema()

class StudentSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    gender = fields.Enum(gender_enum.Gender)
    grade = fields.String(required=True)
    dob = fields.Date("iso")
    
student_schema = StudentSchema()
    

@reg_bp.route('/reg/school', methods=['POST'])
def schoolReg():
    try:
        data = request.get_json()
        schoolData = school_schema.load(data)

        school = School(name=schoolData['school_name'], email=schoolData['email'], 
                        password=schoolData['password'], address=schoolData['address'], 
                        city=schoolData['city'])
        
        storage.new(school)
        storage.save()
        storage.close()

        return jsonify(schoolData), 200
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

        return jsonify(guardianData), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400
    

@reg_bp.route('/reg/student', methods=['POST'])
@jwt_required()
def studentReg():
    try:
        data = request.get_json()
        studentData = student_schema.load(data)
        
        jwt_token = request.headers.get('Authorization')[7:]
        school = util.getInstanceFromJwt(SCHOOL)

        if school == False:
            return jsonify({'message': 'Invalid Credentials'}), 400

        student = Student(first_name=studentData['first_name'], last_name=studentData['last_name'], email=studentData['email'], gender=studentData['gender'], dob=studentData['dob'], grade=studentData['grade'])

        student.school_relation = school

        storage.new(student)
        storage.save()
        storage.close()

        return jsonify(studentData), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400