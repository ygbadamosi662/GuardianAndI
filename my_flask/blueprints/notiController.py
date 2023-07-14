from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

noti_bp = Blueprint('noti', __name__)

# @noti_bp.route('/initiate', methods=['POST'])
# @jwt_required(optional=False)