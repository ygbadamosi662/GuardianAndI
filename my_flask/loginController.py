from flask import Blueprint, request, jsonify
from marshmallow import fields, Schema, ValidationError
from flask_jwt_extended import create_access_token
from models.school import School
from models.guardian import Guardian
from models import storage
from global_variables import globalBcrypt


login_bp = Blueprint('login', __name__)


class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
    
login_schema = LoginSchema()

jwtPayload = {}

@login_bp.route('/login/school', methods=['POST'])
def loginSchool():

    data = request.get_json()
    
    try:
        loginData = login_schema.load(data)

    except ValidationError as err:
        return jsonify({'message': err.messages}), 400
    
    
    session = storage.get_session()
    school = session.query(School).filter_by(email=loginData['email']).first()

    if not school:
        return jsonify({'message': 'Invalid Credentials'}), 400
    
    if not globalBcrypt.checkpw(loginData['password'].encode('utf-8'), school.password.encode('utf-8')):
        return jsonify({'message': 'Invalid Credentials'}), 400
    
    jwtPayload['email'] = loginData['email']
    
    jwt = create_access_token(identity=jwtPayload)

    return jsonify({'jwt': jwt}), 200


@login_bp.route('/login/guardian', methods=['POST'])
def loginGuardian():
    
    data = request.get_json()
    
    try:
        loginData = login_schema.load(data)

    except ValidationError as err:
        return jsonify({'message': err.messages}), 400

    session = storage.get_session()
    guardian = session.query(Guardian).filter_by(email=loginData['email']).first()

    if not guardian:
        return jsonify({'message': 'Invalid Credentials'}), 400
    
    if not globalBcrypt.checkpw(loginData['password'].encode('utf-8'), guardian.password.encode('utf-8')):
        return jsonify({'message': 'Invalid Credentials'}), 400
    
    jwtPayload['email'] = loginData['email']
    
    jwt = create_access_token(identity=jwtPayload)

    return jsonify({'jwt': jwt}), 200