from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from utility import util
# from models import storage
from response_object import getStudentResponse, getListOfResponseObjects, getGuardResponse, getRegistryResponse
from repos.studentRepo import StudentRepo
from repos.guardRepo import GuardRepo, Guard
from repos.guardianRepo import GuardianRepo
from repos.schoolRepo import SchoolRepo, School
from repos.registryRepo import RegistryRepo, Registry
from global_variables import SCHOOL, STUDENT, GUARDIAN, GUARD, REGISTRY
from Enums.tag_enum import Tag
from Enums.status_enum import Status
from schemas import link_schema, update_schema


student_bp = Blueprint('student', __name__)
student_repo = StudentRepo()
guard_repo = GuardRepo()
guardian_repo = GuardianRepo()
school_repo = SchoolRepo()
registry_repo = RegistryRepo()


@student_bp.route('/get/student/<string:email>', methods=['GET'])
@jwt_required(optional=False)
def getStudent(email):
    try:
        if not email:
            return {'Message': 'No unique identifier'}, 400
        
        if util.validate_table_integrity(email, STUDENT) == False:
            return {'Message': 'Invalid Credentials'}, 400

        student = student_repo.findByEmail(email)

        if student:
            return jsonify(getStudentResponse(student)), 200

        return {'Message': 'Invalid Credentials'}, 400
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@student_bp.route('/get/students', methods=['GET'])
@jwt_required(optional=False)
def getStudents():
    try:
        payload = get_jwt_identity()
        if payload['model'] != SCHOOL:
            return {'message': 'Invalid Credentials, only {} allowed'.format(payload['model'])}, 400

        students = util.getInstanceFromJwt().school_students

        return jsonify(getListOfResponseObjects(STUDENT, students, True)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@student_bp.route('/link', methods=['POST'])
@jwt_required(optional=False)
def linkStudent():
    try:
        data = request.get_json()
        linkData = link_schema.load(data)

        payload = get_jwt_identity()
        # check if the user is a guardian
        if payload['model'] != GUARDIAN:
            return {'message': 'Invalid Credentials, only {} allowed'.format(payload['model'])}, 400
        
        if util.validate_table_integrity(linkData['student_email'], STUDENT) == False:
            return {'Message': 'Student does not exist'}, 400
        
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

        return jsonify(getGuardResponse(guard))
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'message': err.args[0]}
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@student_bp.route('/updates/school', methods=['POST'])
@jwt_required(optional=False) 
def backToSchool():
    try:
        data = request.get_json()
        updateData = update_schema.load(data)
       

        payload = get_jwt_identity()
        # checks if model is allowed
        if payload['model'] != GUARDIAN:
            return {'message': 'Invalid Credentials, only {} allowed'.format(payload['model'])}, 400
        
        if util.validate_table_integrity(updateData['student_email'], STUDENT) == False:
            return {'Message': 'Student does not exist'}, 400
        
        student = student_repo.findByEmail(updateData['student_email'])
        # checks if student exist
        if not student:
            return {'message': 'Cant find student {}'.format(updateData['student_email'])}, 400
        
        # checks if school exist
        school = school_repo.findByEmail(updateData['user_email'])
        if school == None:
            return {'message': 'School {} does not exist'.format(updateData['user_email'])}, 400
        
        # check if guardian is an active super-guardian of the student
        if util.isGuardian(student, util.getInstanceFromJwt(), True, True) == False:
            return {'message': 'Inavalid Credentials'}, 400
        
        # checks if student is activeb active student of the provided school already
        if util.ifStudent(student, school):
            return {'message': 'Student {} has an active registry with school {}'.format(updateData['student_email'], updateData['user_email'])}, 400
        
        student.student_school = school
        util.persistModel(student)
        

        # creates registry
        registry = Registry(registry_student=student, registry_school=school, status=Status.ACTIVE)
        # persists registry
        util.persistModel(registry)

        savedRegistry = registry_repo.findByStudentAndStatus(student, Status.ACTIVE)
        
        return jsonify(getRegistryResponse(savedRegistry)), 200
        
        
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'message': err.args[0]}
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
    
@student_bp.route('/remove/school/<email>', methods=['GET'])
@jwt_required(optional=False)
def removeSchool(email):
    try:
        payload = get_jwt_identity()

        if not email:
            return {'Message': 'Cant find nothing with nothing'}, 400
        
        if util.validate_table_integrity(email, STUDENT) == False:
            return {'Message': 'Student does not exist'}, 400

        student = student_repo.findByEmail(email)
            # checks if student exists
        if not student:
            return {'message': 'Student does not exist'}, 400

        # checks if the user is a guardian
        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()

            # checks if user is a guardian, super-guardian and an active guardian to the provided student
            if util.isGuardian(student, guardian,True, True) == False:
                return {'message': 'Invalid Credentials'}, 400

            school = student.student_school
            # checks if student has any active registration
            if school == None:
               return {'message': 'Student {} does not have any active registry at the moment'.format(email)}, 400

        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()

            # checks if student has an active registry with school
            if util.ifStudent(student, school) == False:
                return {'message': 'Student {} has an no active registry with school {}'.format(email, school.email)}, 400

        registry = registry_repo.findByStudentAndSchoolAndStatus(student, school, Status.ACTIVE)
        registry.status = Status.INACTIVE

        student.student_school = None

        util.persistModel(student)
        util.persistModel(registry)

        return jsonify(getRegistryResponse(registry)), 200
    
    except SQLAlchemyError as err:
        return {'message': err.args[0]}
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@student_bp.route('/get/guard/history/<email>/<status>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def getGuards(email, status, page):
    try:
        payload = get_jwt_identity()

        if not email:
            return {'Message': 'Cant find nothing with nothing'}, 400
        
        if util.validate_table_integrity(email, STUDENT) == False:
            return {'Message': 'Student does not exist'}, 400

        student = student_repo.findByEmail(email)

        # checks if student exists
        if not student:
            return {'message': 'Student does not exist'}, 400

        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()

            registry = registry_repo.findByStudentAndSchoolAndStatus(student, school, Status.ACTIVE)

            # checks if registry is Active
            if not registry:
                return {'message': 'student does not have an active registration with your school'}, 400

        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()

            guard = guard_repo.findByStudentAndGuardianAndStatus(student, guardian, Status.ACTIVE)

            # checks if guard is active
            if not guard:
                return {'message': 'You are not an active guardian to the student'}, 400

        realStatus = {}
        if status == 'active':
            realStatus = Status.ACTIVE

        if status == 'inactive':
            realStatus = Status.INACTIVE

        guards = guard_repo.pageByStudentAndStatus(student, realStatus, page)

        return jsonify(getListOfResponseObjects(GUARD, guards, True)), 200
    
    except SQLAlchemyError as err:
        return {'message': err.args[0]}
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@student_bp.route('/get/registry/history/<email>/<status>/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def getGuardianGuardHistory(email, status, page):
    try:
        payload = get_jwt_identity()
        if not email:
            return {'Message': 'Cant find nothing with nothing'}, 400
        
        if util.validate_table_integrity(email, STUDENT) == False:
            return {'Message': 'Student does not exist'}, 400

        student = student_repo.findByEmail(email)

        # checks if student exists
        if not student:
            return {'message': 'Student does not exist'}, 400

        if payload['model'] == SCHOOL:
            school = util.getInstanceFromJwt()

            registry = registry_repo.findByStudentAndSchoolAndStatus(student, school, Status.ACTIVE)

            # checks if registry is Active
            if not registry:
                return {'message': 'student does not have an active registration with your school'}, 400

        if payload['model'] == GUARDIAN:
            guardian = util.getInstanceFromJwt()

            guard = guard_repo.findByStudentAndGuardianAndStatus(student, guardian, Status.ACTIVE)

            # checks if guard is active
            if not guard:
                return {'message': 'You are not an active guardian to the student'}, 400

        realStatus = {}
        if status == 'active':
            realStatus = Status.ACTIVE

        if status == 'inactive':
            realStatus = Status.INACTIVE    

        registries = registry_repo.pageByStudentAndStatus(student, realStatus, page)
        
        return jsonify(getListOfResponseObjects(REGISTRY, registries, True)), 200
    
    except SQLAlchemyError as err:
        return {'message': err.args[0]}
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()