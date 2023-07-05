"""Defines methods that returns response objects(dict) of our models"""
from models.student import Student
from models.school import School
from models.guardian import Guardian
from global_variables import SCHOOL, GUARDIAN, STUDENT

def getSchoolResponse(school: School) -> dict:
    schoolObj = {}
    schoolObj['name'] = school.name
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
    studentObj['school'] = getSchoolResponse(student.student_school)

    return studentObj

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