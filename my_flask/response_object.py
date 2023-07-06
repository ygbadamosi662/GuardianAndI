"""Defines methods that returns response objects(dict) of our models"""
from models.student import Student
from models.school import School
from models.guardian import Guardian
from models.guard import Guard
from models.registry import Registry
from models import storage
from global_variables import SCHOOL, GUARDIAN, STUDENT

def getSchoolResponse(school: School) -> dict:
    schoolObj = {}
    schoolObj['name'] = school.school_name
    schoolObj['email'] = school.email
    schoolObj['address'] = school.address
    schoolObj['city'] = school.city

    return schoolObj

def getGuardianResponse(guardian: Guardian) -> dict:
    guardianObj = {}
    guardianObj['name'] = guardian.first_name + " " + guardian.last_name
    guardianObj['email'] = guardian.email
    guardianObj['gender'] = guardian.gender.value

    return guardianObj

def getStudentResponse(student: Student) -> dict:
    studentObj = {}
    studentObj['name'] = student.first_name + " " + student.last_name
    studentObj['email'] = student.email
    studentObj['gender'] = student.gender.value
    studentObj['grade'] = student.grade
    studentObj['dob'] = student.dob
    session = storage.get_session()
    school = session.get(Student, student.id).student_school
    if school:
        studentObj['school'] = getSchoolResponse(school)

    return studentObj

def getGuardResponse(guard: Guard) -> dict:
    guardObj = {}
    guard_ish = storage.get_session().get(Guard, guard.id)

    guardObj['student'] = getStudentResponse(guard_ish.guard_student)
    guardObj['guardian'] = getGuardianResponse(guard_ish.guard_guardian)
    guardObj['tag'] = guard.tag.value
    guardObj['status'] = guard.status.value

    return guardObj

def getListOfResponseObjects(modelType, models) -> list:
    objList = []
    if modelType == STUDENT:
        for model in models:
            objList.append(getStudentResponse(model))
        return objList

    if modelType == SCHOOL:
        for model in models:
            objList.append(getSchoolResponse(model))
        return objList
    
    if modelType == GUARDIAN:
        for model in models:
            objList.append(getGuardianResponse(model))
        return objList
    
def getRegistryResponse(registry: Registry) -> dict:
    registryObj = {}
    session = storage.get_session()
    regi = session.get(Registry, registry.id)
    registryObj['student'] = getStudentResponse(regi.registry_student)
    registryObj['school'] = getSchoolResponse(regi.registry_school)
    registryObj['status'] = registry.status.value

    return registryObj
