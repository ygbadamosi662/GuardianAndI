from flask import Blueprint, request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, ValidationError, validate
from models import storage
from models.school import School
from models.guardian import Guardian
from models.student import Student


reg_bp = Blueprint('reg', __name__)
ma = Marshmallow(reg_bp)


class SchoolSchema(Schema):
    name = fields.String(required=True)
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
    gender = fields.String(required=True, validate=validate.OneOf(["MALE", "FEMALE"]))
    dob = fields.Date("iso")

guardian_schema = GuardianSchema()

class StudentSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(["MALE", "FEMALE"]))
    grade = fields.String(required=True)
    dob = fields.Date("iso")
    schoolEmail = fields.String(required=True)

student_schema = StudentSchema()
    

@reg_bp.route('/home')
def home():
    # session = storage.get_session()
    # storage.deleteAll()
    # session.query(Student).delete()
    # session.commit()
    return jsonify("welcome home")

@reg_bp.route('/reg/school', methods=['POST'])
def schoolReg():
    try:
        data = request.get_json()
        schoolData = school_schema.load(data)

        school = School(name=schoolData['name'], email=schoolData['email'], 
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
def studentReg():  
    try:
        data = request.get_json()
        studentData = student_schema.load(data)

        session = storage.get_session()
        school = session.query(School).filter_by(email=studentData['schoolEmail']).first()

        if not school:
            return "Cant find school, school is not registered on our platform", 400

        student = Student(first_name=studentData['first_name'], last_name=studentData['last_name'], email=studentData['email'], gender=studentData['gender'], dob=studentData['dob'], grade=studentData['grade'])

        student.school_relation = school

        storage.new(student)
        storage.save()
        storage.close()

        return jsonify(studentData), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400