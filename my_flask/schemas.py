"""Defines schemas using marshmallow for our request and response dtos"""
from marshmallow import fields, Schema
from Enums.gender_enum import Gender
from Enums.tag_enum import Tag


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

class LinkStudent(Schema):
    guardian_email = fields.Email(required=True)
    student_email = fields.Email(required=True)
    tag = fields.Enum(Tag)

link_schema = LinkStudent()

class UpdateSchool(Schema):
    user_email = fields.Email(required=True)
    student_email = fields.Email(required=True)

update_schema = UpdateSchool()

class PadSchema(Schema):
    user_email = fields.Email(required=True)
    student_email = fields.Email(required=True)
    action = fields.String(required=True)

pad_schema = PadSchema()

class StudentPadSchema(Schema):
    student_email = fields.Email(required=True)
    filter = fields.String(required=True)
    action = fields.String(required=True)
    page = fields.Number(required=True)

student_pad_schema = StudentPadSchema()

class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
    
login_schema = LoginSchema()