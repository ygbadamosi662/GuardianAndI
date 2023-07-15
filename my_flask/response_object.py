"""Defines methods that returns response objects(dict) of our models"""
from models.student import Student
from models.school import School
from models.guardian import Guardian
from models.guard import Guard
from models.registry import Registry
from models.pick_and_drop import PickAndDrop
from models.notification import Notification
from models import storage
from global_variables import SCHOOL, GUARDIAN, STUDENT, GUARD, REGISTRY, PICK_AND_DROP, NOTIFICATION

def getSchoolResponse(school: School) -> dict:
    if school:
        schoolObj = {}
        schoolObj['id'] = school.id
        schoolObj['name'] = school.school_name
        schoolObj['email'] = school.email
        schoolObj['address'] = school.address
        schoolObj['city'] = school.city

        return schoolObj

def getGuardianResponse(guardian: Guardian) -> dict:
    if guardian:
        guardianObj = {}
        guardianObj['id'] = guardian.id
        guardianObj['name'] = guardian.first_name + " " + guardian.last_name
        guardianObj['email'] = guardian.email
        guardianObj['gender'] = guardian.gender.value

        return guardianObj

def getStudentResponse(student: Student, pure: bool = False) -> dict:
    if student:
        studentObj = {}
        studentObj['id'] = student.id
        studentObj['name'] = student.first_name + " " + student.last_name
        studentObj['email'] = student.email
        studentObj['gender'] = student.gender.value
        studentObj['grade'] = student.grade
        studentObj['dob'] = student.dob

        if pure:
            return studentObj

        session = storage.get_session()
        school = session.get(Student, student.id).student_school
        if school:
            studentObj['school'] = getSchoolResponse(school)

        return studentObj

def getGuardResponse(guard: Guard) -> dict:
    if guard:
        guardObj = {}
        guard_ish = storage.get_session().get(Guard, guard.id)

        guardObj['id'] = guard.id
        guardObj['student'] = getStudentResponse(guard_ish.guard_student, True)
        guardObj['guardian'] = getGuardianResponse(guard_ish.guard_guardian)
        guardObj['tag'] = guard.tag.value
        guardObj['status'] = guard.status.value

        return guardObj

def getRegistryResponse(registry: Registry) -> dict:
    if registry:
        registryObj = {}
        session = storage.get_session()
        regi = session.get(Registry, registry.id)
        registryObj['id'] = registry.id
        registryObj['student'] = getStudentResponse(regi.registry_student, True)
        registryObj['school'] = getSchoolResponse(regi.registry_school)
        registryObj['status'] = registry.status.value

        return registryObj

def getPadResponse(pad: PickAndDrop) -> dict:
    if pad:
        padObj = {}

        padObj['id'] = pad.id
        session = storage.get_session()
        pad_ish = session.get(PickAndDrop, pad.id)
        padObj['registry'] = getRegistryResponse(pad_ish.PAD_registry)
        padObj['guard'] = getGuardResponse(pad_ish.PAD_guard)
        padObj['auth'] = pad.auth.value
        padObj['action'] = pad.action.value
        padObj['auth_provider'] = getGuardianResponse(pad_ish.auth_provider)

        return padObj

def getNotiResponse(noti: Notification) -> dict:
    if noti:
        notiObj = {}
        notiObj['id'] = noti.id

        session = storage.get_session()
        noti_ish = session.get(Notification, noti.id)

        notiObj['activity'] = noti.activity.value
        notiObj['permit'] = noti.permit.value
        notiObj['note'] = noti.note
        # setting sender
        if noti_ish.note_sender.__tablename__ == SCHOOL:
            notiObj['sender'] = getSchoolResponse(noti_ish.note_sender)

        if noti_ish.note_sender.__tablename__ == GUARDIAN:
            notiObj['sender'] = getGuardianResponse(noti_ish.note_sender)

        # setting receiver
        if noti_ish.note_receiver.__tablename__ == SCHOOL:
            notiObj['receiver'] = getSchoolResponse(noti_ish.note_receiver)

        if noti_ish.note_receiver.__tablename__ == GUARDIAN:
            notiObj['receiver'] = getGuardianResponse(noti_ish.note_receiver)

        # setting subject
        if noti_ish.subject.__tablename__ == REGISTRY:
            notiObj['subject'] = getRegistryResponse(noti_ish.subject)

        if noti_ish.subject.__tablename__ == GUARD:
            notiObj['subject'] = getGuardResponse(noti_ish.subject)

        if noti_ish.subject.__tablename__ == PICK_AND_DROP:
            notiObj['subject'] = getPadResponse(noti_ish.subject)

        if noti_ish.subject.__tablename__ == STUDENT:
            notiObj['subject'] = getStudentResponse(noti_ish.subject, True)

        return notiObj

def getListOfResponseObjects(modelType, models: list, pure: bool = False) -> list:
    if modelType and models:
        objList = []
        if modelType == STUDENT:
            for model in models:
                objList.append(getStudentResponse(model, pure))
            return objList

        if modelType == SCHOOL:
            for model in models:
                objList.append(getSchoolResponse(model))
            return objList

        if modelType == GUARDIAN:
            for model in models:
                objList.append(getGuardianResponse(model))
            return objList

        if modelType == GUARD:
            for model in models:
                objList.append(getGuardResponse(model))
            return objList

        if modelType == REGISTRY:
            for model in models:
                objList.append(getRegistryResponse(model))
            return objList

        if modelType == PICK_AND_DROP:
            for model in models:
                objList.append(getPadResponse(model))
            return objList
        
        if modelType == NOTIFICATION:
            for model in models:
                objList.append(getNotiResponse(model))
            return objList

