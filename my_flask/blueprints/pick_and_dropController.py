from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from schemas import pad_schema
from models.pick_and_drop import PickAndDrop
from response_object import getListOfResponseObjects, getPadResponse
from models import storage
from global_variables import GUARD, GUARDIAN, SCHOOL, PICK_AND_DROP, REGISTRY, STUDENT
from utility import util
from Enums.status_enum import Status
from Enums.auth_enum import Auth
from Enums.action_enum import Action
from Enums.tag_enum import Tag
from repos.guardianRepo import guardian_repo
from repos.guardRepo import guard_repo
from repos.notificationRepo import note_repo
from repos.pick_and_dropRepo import pad_repo
from repos.registryRepo import registry_repo
from repos.schoolRepo import school_repo
from repos.studentRepo import student_repo


pad_bp = Blueprint('pad', __name__)


@pad_bp.route('/initiate', methods=['POST'])
@jwt_required(optional=False)
def initiateDrop():
    # storage.get_session().rollback()
    payload = get_jwt_identity()
    # checks credentials
    if payload['model'] != GUARDIAN:
        return {'message': 'Invalid Credentials'}, 400
    
    try:
        data = request.get_json()
        padData = pad_schema.load(data)
        print(padData)

        student = student_repo.findByEmail(padData['student_email'])

        # checks if student exist
        if not student:
            return {'message': 'student does not exist'}, 400
        
        guardian = util.getInstanceFromJwt()
        
        guard = guard_repo.findByStudentAndGuardianAndStatus(student, guardian, Status.ACTIVE)
        # checks if guard valid
        if not guard:
            return {'message': 'Inavalid Credentials'}, 400
        
        # write a check if guardian has open pad
        
        registry = {}
        
        registry = registry_repo.findByStudentAndStatus(student, Status.ACTIVE)
        if not registry:
            return {'message': 'Student does not have any active registration'}
        
        if util.check_for_active_pad(registry):
            return {'message': 'Student already in play'}, 400
        
        actor = {}
        if padData['action'] == 'pick':
            actor = Action.PICK_UP
            
        if padData['action'] == 'drop':
            actor = Action.DROP_OFF
        
        pad = PickAndDrop(PAD_registry=registry, PAD_guard= guard, action=actor, auth=Auth.initiate())
        
        util.persistModel(pad)
        
        pad = util.check_for_active_pad(registry, True)
        util.closeSession()

        return jsonify(getPadResponse(pad)), 400
    except ValidationError as err:
        return {'message': err.messages}, 400