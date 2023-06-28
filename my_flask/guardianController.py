from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
jwt = JWTManager(app)

# Route for generating JWT token
@app.route('/login', methods=['POST'])
def login():
    # Perform user authentication logic
    # ...

    # If authentication is successful, generate JWT token
    access_token = create_access_token(identity=user_id)
    return {'access_token': access_token}

# Protected route that requires JWT authentication
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Handle the protected route logic
    # ...
    return 'Access granted!'

if __name__ == '__main__':
    app.run()