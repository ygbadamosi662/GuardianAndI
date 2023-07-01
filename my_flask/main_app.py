from flask import Flask
from regController import reg_bp
from loginController import login_bp
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

jtw_manager = JWTManager(app)
ma = Marshmallow(app)


app.register_blueprint(reg_bp, url_prefix='/api/v1')
app.register_blueprint(login_bp, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run()