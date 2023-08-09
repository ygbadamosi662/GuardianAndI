from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from marshmallow import ValidationError
from services.note_service import note_service
from models.school import School
from models.guardian import Guardian
from models.student import Student
from models.registry import Registry
from  models.jwt_blacklist import Jwt_Blacklist
from models.guard import Guard
from sqlalchemy.exc import SQLAlchemyError
from response_object import getSchoolResponse, getGuardianResponse, getStudentResponse
from schemas import student_schema, school_schema, guardian_schema, login_schema, profile_update_schema
from utility import util
from global_variables import SCHOOL, GUARDIAN, STUDENT, AUTHORIZATION, CONFIRMATION, globalBcrypt
from repos.schoolRepo import school_repo
from repos.guardianRepo import guardian_repo
from repos.studentRepo import student_repo
from Enums.tag_enum import Tag
from Enums.status_enum import Status
from Enums.permit_enum import Permit


user_bp = Blueprint('user', __name__)

@user_bp.route('/reg/school', methods=['POST'])
def schoolReg():
    try:
        data = request.get_json()
        schoolData = school_schema.load(data)

        # checks table integrity
        if util.validate_table_integrity_byEmail(schoolData['email'], SCHOOL):
            return {'Message': '{} already exists'.format(schoolData['email'])}, 400
        
        # checks phone number uniqueness
        if util.validate_table_integrity_byPhone(schoolData['phone'], SCHOOL):
            return {'Message': '{} already exists'.format(schoolData['phone'])}, 400

        school = School(school_name=schoolData['school_name'], email=schoolData['email'], 
                        password=schoolData['password'], address=schoolData['address'], 
                        city=schoolData['city'], phone=schoolData['phone'])
        
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
    
@user_bp.route('/reg/guardian', methods=['POST'])
def guardianReg():  
    try:
        data = request.get_json()
        guardianData = guardian_schema.load(data)

        # checks table integrity
        if util.validate_table_integrity_byEmail(guardianData['email'], GUARDIAN):
            return {'Message': '{} already exists'.format(guardianData['email'])}, 400
        
        # checks phone numbers uniqueness
        if util.validate_table_integrity_byEmail(guardianData['phone'], GUARDIAN):
            return {'Message': '{} already exists'.format(guardianData['phone'])}, 400

        guardian = Guardian(first_name=guardianData['first_name'], last_name=guardianData['last_name'], email=guardianData['email'], password=guardianData['password'], gender=guardianData['gender'], dob=guardianData['dob'], phone=guardianData['phone'])
        
        util.persistModel(guardian)

        return jsonify(guardian_schema.dump(guardianData)), 200
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@user_bp.route('/reg/student', methods=['POST'])
@jwt_required()
def studentReg():
    try:
        # checks if jwt_toke is blacklisted
        if util.validate_against_jwt_blacklist():
            return {'Message': 'Your session has expired, login again'}, 400
        
        data = request.get_json()
        payload = get_jwt_identity()

        studentData = student_schema.load(data)

        if payload['model'] == SCHOOL:

            school = util.getInstanceFromJwt()

            if util.validate_table_integrity_byEmail(studentData['email'], STUDENT):
                student = student_repo.findByEmail(studentData['email'])
                if student.student_school:
                    if student.student_school == school:
                        return {'Message': 'Student is alraedy registered to your school'}, 400

                return {'Message': 'Student {} already exists and have an active registration'.format(studentData['email'])}, 400

            # checks if guardian exist
            if util.validate_table_integrity_byEmail(studentData['user_email'], GUARDIAN) == False:
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

            if util.validate_table_integrity_byEmail(studentData['email'], STUDENT):
                if util.student_validate_guardian(student_repo.findByEmail(studentData['email']), util.getInstanceFromJwt()):
                    return {'Message': 'Student already registere and linked to you'}, 400
                
                return {'Message': 'Student exists already'}, 400

            # check if school exists
            if util.validate_table_integrity_byEmail(studentData['user_email'], SCHOOL) == False:
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

@user_bp.route('/login/school', methods=['POST'])
def loginSchool():
    data = request.get_json()
    
    try:
        loginData = login_schema.load(data)

        if util.validate_table_integrity_byEmail(loginData['email'], SCHOOL) == False:
            return {'Message': 'Invalid Credentials'}

        school = school_repo.findByEmail(loginData['email'])

        if not school:
            return {'message': 'Invalid Credentials, only {} is allowed'.format(SCHOOL)}, 401

        if not globalBcrypt.checkpw(loginData['password'].encode('utf-8'), school.password.encode('utf-8')):
            return jsonify({'message': 'Invalid Credentials'}), 401

        jwt = create_access_token(identity={'email': loginData['email'], 'model': SCHOOL})

        return jsonify({'jwt': jwt}), 201
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@user_bp.route('/login/guardian', methods=['POST'])
def loginGuardian():
    
    data = request.get_json()
    
    try:
        loginData = login_schema.load(data)

        if util.validate_table_integrity_byEmail(loginData['email'], GUARDIAN) == False:
            return {'Message': 'Invalid Credentials'}

        guardian = guardian_repo.findByEmail(loginData['email'])

        if not guardian:
            return jsonify({'message': 'Invalid Credentials, only {} is allowed'.format(GUARDIAN)}), 400

        if not globalBcrypt.checkpw(loginData['password'].encode('utf-8'), guardian.password.encode('utf-8')):
            return jsonify({'message': 'Invalid Credentials'}), 401

        jwt = create_access_token(identity={'email': loginData['email'], 'model': GUARDIAN})

        return jsonify({'jwt': jwt}), 201
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@user_bp.route('/signout', methods=['GET'])
@jwt_required(optional=False)
def signout():
    try:
        jwt_token = request.headers.get('Authorization')[7:]
        user = util.getInstanceFromJwt()

        blacklist = Jwt_Blacklist(jwt=jwt_token, user=user)
        util.persistModel(blacklist)
        
        return {'Message': 'Signed out successfully'}, 201
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@user_bp.route('/profile', methods=['POST'])
@jwt_required(optional=False)
def update_profile():
    try:
        # checks if jwt_toke is blacklisted
        if util.validate_against_jwt_blacklist():
            return {'Message': 'Your session has expired, login again'}, 400
        
        # extracts set data
        setData = util.extract_set_data_from_schema(profile_update_schema.load(request.get_json()))
        if not setData:
            return {'Message': 'Update what?'}, 400

        user = util.getInstanceFromJwt()

        return jsonify(getSchoolResponse(util.update_profile(setData, user))), 200

    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
