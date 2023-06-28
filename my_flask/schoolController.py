from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, ValidationError
from models import storage
from models.school import School
import bcrypt

app = Flask(__name__)
ma = Marshmallow(app)

class SchoolSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    address = fields.String(required=True)
    city = fields.String(required=True)

school_schema = SchoolSchema()


@app.route('/school/reg', methods=['POST'])
def reg():
    try:
        # Validate the request data against the schema
        data = request.get_json()
        schoolData = school_schema.load(data)

        school = School(name=schoolData['name'], email=schoolData['email'], 
                        password=schoolData['password'], address=schoolData['address'], city=schoolData['city'])
        storage.new(school)
        storage.save()
        storage.close()

        return jsonify(schoolData), 200
    except ValidationError as err:
        # Handle validation errors
        return {'errors': err.messages}, 400

@app.route('/home')
def shit():
    return jsonify('shit')


if __name__ == '__main__':
    app.run()