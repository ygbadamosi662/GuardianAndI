from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from marshmallow import fields, Schema, ValidationError


student_bp = Blueprint('student', __name__)


# @student_bp.route('/students', methods=['POST'])
# @jwt_required
# def getStudents():

