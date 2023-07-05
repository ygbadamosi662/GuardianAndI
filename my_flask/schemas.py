"""Defines schemas using marshmallow for our request and response dtos"""
from marshmallow import fields, Schema
from Enums.gender_enum import Gender


class SchoolSchema(Schema):
    school_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    address = fields.String(required=True)
    city = fields.String(required=True)

school_schema = SchoolSchema()

class GuardianSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    gender = fields.Enum(Gender)
    dob = fields.Date("iso")

guardian_schema = GuardianSchema()

class StudentSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    gender = fields.Enum(Gender)
    grade = fields.String(required=True)
    dob = fields.Date("iso")
    
student_schema = StudentSchema()