from flask import Blueprint, request, jsonify
from marshmallow import fields, Schema, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token
from models.school import School
from models.guardian import Guardian
from models import storage
from utility import util
from repos.guardianRepo import guardian_repo
from repos.schoolRepo import school_repo
from global_variables import globalBcrypt, GUARDIAN, SCHOOL


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

        if util.validate_table_integrity(loginData['email'], SCHOOL) == False:
            return {'Message': 'Invalid Credentials'}

        school = school_repo.findByEmail(loginData['email'])

        if not school:
            return {'message': 'Invalid Credentials, only {} is allowed'.format(SCHOOL)}, 401

        if not globalBcrypt.checkpw(loginData['password'].encode('utf-8'), school.password.encode('utf-8')):
            return jsonify({'message': 'Invalid Credentials'}), 401

        jwtPayload['email'] = loginData['email']
        jwtPayload['model'] = SCHOOL

        jwt = create_access_token(identity=jwtPayload)

        return jsonify({'jwt': jwt}), 201
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()


@login_bp.route('/login/guardian', methods=['POST'])
def loginGuardian():
    
    data = request.get_json()
    
    try:
        loginData = login_schema.load(data)

        if util.validate_table_integrity(loginData['email'], GUARDIAN) == False:
            return {'Message': 'Invalid Credentials'}

        guardian = guardian_repo.findByEmail(loginData['email'])

        if not guardian:
            return jsonify({'message': 'Invalid Credentials, only {} is allowed'.format(GUARDIAN)}), 400

        if not globalBcrypt.checkpw(loginData['password'].encode('utf-8'), guardian.password.encode('utf-8')):
            return jsonify({'message': 'Invalid Credentials'}), 401

        jwtPayload['email'] = loginData['email']
        jwtPayload['model'] = GUARDIAN

        jwt = create_access_token(identity=jwtPayload)

        return jsonify({'jwt': jwt}), 201
    
    except ValidationError as err:
        return {'message': err.args[0]}, 400
    except TypeError as err:
        return {'Message': err.args[0]}, 400
    except SQLAlchemyError as err:
        return {'Message': err.args[0]}, 400
    finally:
        util.closeSession()