from flask import Flask, jsonify, current_app
from regController import reg_bp
from loginController import login_bp
from studentController import student_bp
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import Config
from models import storage
# from models.student import Student


app = Flask(__name__)
app.config.from_object(Config)



jwt_manager = JWTManager(app)
ma = Marshmallow(app)

path_prefix = '/api/v1'

app.register_blueprint(reg_bp, url_prefix=path_prefix)
app.register_blueprint(login_bp, url_prefix=path_prefix)
app.register_blueprint(student_bp, url_prefix=path_prefix)

with app.app_context():
    secret = current_app.config.get('JWT_SECRET_KEY')
    print(secret)

@app.route('/')
def home():
    # session = storage.get_session()
    storage.deleteAll()
    # session.query(Student).delete()
    # session.commit()
    return jsonify("welcome home")

if __name__ == '__main__':
    app.run()