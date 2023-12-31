from flask import Flask, jsonify
from blueprints.userController import user_bp
from blueprints.studentController import student_bp
from blueprints.schoolController import school_bp
from blueprints.guardianController import guardian_bp
from blueprints.pick_and_dropController import pad_bp
from blueprints.notiController import noti_bp
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import Config
from models import storage
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.user_admin import UserAdmin
# from models.student import Student


app = Flask(__name__)
app.config.from_object(Config)

jwt_manager = JWTManager(app)
ma = Marshmallow(app)

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(UserAdmin, storage.get_session()))

path_prefix = '/api/v1'

app.register_blueprint(user_bp, url_prefix=path_prefix+'/user')
app.register_blueprint(student_bp, url_prefix=path_prefix+'/student')
app.register_blueprint(school_bp, url_prefix=path_prefix+'/school')
app.register_blueprint(guardian_bp, url_prefix=path_prefix+'/guardian')
app.register_blueprint(pad_bp, url_prefix=path_prefix+'/pad')
app.register_blueprint(noti_bp, url_prefix=path_prefix+'/noti')

# with app.app_context():
#     secret = current_app.config.get('JWT_SECRET_KEY')
#     print(secret)

@app.route('/')
def home():
    # session = storage.get_session()
    storage.deleteAll()
    # session.query(Student).delete()
    # session.commit()
    return jsonify("welcome home")

if __name__ == '__main__':
    app.run()
