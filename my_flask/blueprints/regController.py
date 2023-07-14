from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, Schema, ValidationError
from services.note_service import note_service
from models.school import School
from models.guardian import Guardian
from models.student import Student
from models.registry import Registry
from models.guard import Guard
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy import exc as sa_exc
# from models.notification import Notification
from utility import util
from global_variables import SCHOOL, GUARDIAN, STUDENT, AUTHORIZATION, CONFIRMATION
from repos.studentRepo import StudentRepo
from repos.guardianRepo import GuardianRepo
from repos.schoolRepo import SchoolRepo
from Enums.gender_enum import Gender
from Enums.tag_enum import Tag
from Enums.status_enum import Status
from Enums.permit_enum import Permit


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

def validate_length(value, school):
    if value != school:
        raise ValidationError("Invalid credential")

class StudentSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    gender = fields.Enum(Gender)
    grade = fields.String(required=True)
    dob = fields.Date("iso")
    user_email = fields.Email(required=True)
    
student_schema = StudentSchema()


student_repo = StudentRepo()
school_repo = SchoolRepo()
guardian_repo = GuardianRepo()

    

@reg_bp.route('/reg/school', methods=['POST'])
def schoolReg():
    try:
        data = request.get_json()
        schoolData = school_schema.load(data)

        # checks table integrity
        if util.validate_table_integrity(schoolData['email'], SCHOOL):
            return {'Message': '{} already exists'.format(schoolData['email'])}, 400

        school = School(school_name=schoolData['school_name'], email=schoolData['email'], 
                        password=schoolData['password'], address=schoolData['address'], 
                        city=schoolData['city'])
        
        util.persistModel(school)
        
        return jsonify(school_schema.dump(schoolData)), 200
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
    
@reg_bp.route('/reg/guardian', methods=['POST'])
def guardianReg():  
    try:
        data = request.get_json()
        guardianData = guardian_schema.load(data)

        # checks table integrity
        if util.validate_table_integrity(guardianData['email'], GUARDIAN):
            return {'Message': '{} already exists'.format(guardianData['email'])}, 400

        guardian = Guardian(first_name=guardianData['first_name'], last_name=guardianData['last_name'], email=guardianData['email'], password=guardianData['password'], gender=guardianData['gender'], dob=guardianData['dob'])
        
        util.persistModel(guardian)
        util.closeSession()

        return jsonify(guardian_schema.dump(guardianData)), 200
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@reg_bp.route('/reg/student', methods=['POST'])
@jwt_required()
def studentReg():
    try:
        data = request.get_json()
        payload = get_jwt_identity()

        studentData = student_schema.load(data)

        if payload['model'] == SCHOOL:

            school = util.getInstanceFromJwt()

            if util.validate_table_integrity(studentData['email'], STUDENT):
                student = student_repo.findByEmail(studentData['email'])
                if student.student_school:
                    if student.student_school == school:
                        return {'Message': 'Student is alraedy registered to your school'}, 400

                return {'Message': 'Student {} already exists and have an active registration'.format(studentData['email'])}, 400

            # checks if guardian exist
            if util.validate_table_integrity(studentData['user_email'], GUARDIAN) == False:
                return {'message': 'Guardian {} does not exist in our world'.format(studentData['user_email'])}, 400
            
            guardian = guardian_repo.findByEmail(studentData['user_email'])
           
            student = Student(first_name=studentData['first_name'], last_name=studentData['last_name'], email=studentData['email'], gender=studentData['gender'], dob=studentData['dob'], grade=studentData['grade'])
            # student.student_school = school
            util.persistModel(student)
            student = student_repo.findByEmail(studentData['email'])

            registry = Registry(registry_student=student, registry_school=school, status=Status.ACTIVE_GYELLOW)
            util.persistModel(registry)
            
            # We are assuming here the school has done its due diligence on the guardian information they have provided
            guard = Guard(guard_student=student, guard_guardian=guardian, tag=Tag.SUPER_GUARDIAN, status=Status.ACTIVE)
            util.persistModel(guard)

            # notify the guardian
            note_service.create_noti(school, guardian, registry, Permit.READ_AND_WRITE, AUTHORIZATION)
            note_service.create_noti(school, guardian, guard, Permit.READ_AND_WRITE, CONFIRMATION)

        
        if payload['model'] == GUARDIAN:

            if util.validate_table_integrity(studentData['email'], STUDENT):
                if util.student_validate_guardian(student_repo.findByEmail(studentData['email']), util.getInstanceFromJwt()):
                    return {'Message': 'Student already registere and linked to you'}, 400
                
                return {'Message': 'Student exists already'}, 400

            # check if school exists
            if util.validate_table_integrity(studentData['user_email'], SCHOOL) == False:
                return {'message': 'School {} does not exist in our world'.format(studentData['user_email'])}, 400

            school = school_repo.findByEmail(studentData['user_email'])
            
            guardian = util.getInstanceFromJwt()
           
            student = Student(first_name=studentData['first_name'], last_name=studentData['last_name'], email=studentData['email'], gender=studentData['gender'], dob=studentData['dob'], grade=studentData['grade'])
            student.student_school = school
            util.persistModel(student)
            student = student_repo.findByEmail(studentData['email'])

            registry = Registry(registry_student=student, registry_school=school, status=Status.ACTIVE_SYELLOW)
            util.persistModel(registry)

            guard = Guard(guard_student=student, guard_guardian=guardian, tag=Tag.SUPER_GUARDIAN, status=Status.ACTIVE)
            util.persistModel(guard)

            # notify the school
            note_service.create_noti(guardian, school, registry, Permit.READ_AND_WRITE, CONFIRMATION)
       
        
        return jsonify(student_schema.dump(studentData)), 200

    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()