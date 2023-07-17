"""Defines schemas using marshmallow for our request and response dtos"""
from marshmallow import fields, Schema, ValidationError
import re
from Enums.gender_enum import Gender
from Enums.tag_enum import Tag

def validate_phone_number(phone_number):
    # checks if the phone number matches (8 or 7 or 9 or 2)(0 or 1)(then any number from 0-9 8 times), the leading 0 in nigerian phone numbers is ignored in this case, so it expects a nigerian number without the leading 0
    pattern = r'^[8792][01]\d{8}$'
    if not re.match(pattern, phone_number):
        raise ValidationError('Invalid phone number format')



class SchoolSchema(Schema):
    school_name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(validate=validate_phone_number, required=True)
    password = fields.String(required=True)
    address = fields.String(required=True)
    city = fields.String(required=True)

school_schema = SchoolSchema()

class GuardianSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(validate=validate_phone_number, required=True)
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

class UpdateSchool_Sc(Schema):
    email = fields.Email(required=True)

update_sc_schema = UpdateSchool_Sc()

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

class ProfileUpdate(Schema):
    school_name = fields.String()
    address = fields.String()
    city = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    phone = fields.String(validate=validate_phone_number)

profile_update_schema = ProfileUpdate()
    