from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from response_object import getNotiResponse, getListOfResponseObjects
from global_variables import NOTIFICATION
from marshmallow import ValidationError
from Enums.activity_enum import Activity
from Enums.permit_enum import Permit
from sqlalchemy.exc import SQLAlchemyError
from utility import util
from services.note_service import note_service
from repos.notificationRepo import note_repo


noti_bp = Blueprint('noti', __name__)

@noti_bp.route('/get/notis/<int:page>', methods=['GET'])
@jwt_required(optional=False)
def get_notifications(page):
    try:
        user = util.getInstanceFromJwt()
        return jsonify(getListOfResponseObjects(NOTIFICATION, note_service.get_needy_notis(user, page))), 200

    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()

@noti_bp.route('/update/<int:id>', methods=['GET'])
@jwt_required(optional=False)
def update_notifications(id):
    try:
        noti = note_repo.findById(id)
        if not noti:
            return {'Message': 'Cant find notification'}, 400
        
        user = util.getInstanceFromJwt()
        if user != noti.note_receiver:
            return {'Message': 'Invalid Credentials'}, 400
        
        if noti.activity == Activity.DONE:
            return {'Message': 'No further action required'}, 400
        
        if (noti.activity == Activity.SEEN) and (noti.permit != Permit.READ_AND_WRITE):
            return {'Message': 'No further action required'}, 400
        
        if noti.activity == Activity.SENT:
            noti.activity = Activity.DELIVERED
            util.persistModel(noti)
            return jsonify(getNotiResponse(noti)), 200

        if noti.activity == Activity.DELIVERED:
            noti.activity = Activity.SEEN
            util.persistModel(noti)
            return jsonify(getNotiResponse(noti)), 200

        if noti.activity == Activity.SEEN:
            noti.activity = Activity.DONE
            util.persistModel(noti)
            return jsonify(getNotiResponse(noti)), 200
    
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()
    