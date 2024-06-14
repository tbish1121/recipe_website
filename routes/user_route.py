from flask import Blueprint, request, abort, jsonify, make_response
from ..extensions import db
from ..models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies, create_refresh_token

user_route = Blueprint('user_route', __name__)

#Create a user
@user_route.route('/api/register', methods=['POST'])
def create_user():
        data = request.json

        if not data['username'] or not data['password']:
            abort(400, 'Both username and password are required')
        
        if User.query.filter_by(username=data['username']).first():
            abort(400, 'Username already exists')
        
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}
        
#Login User
@user_route.route('/api/login', methods=['POST'])
def login_user():
     data = request.json

     username = data['username']
     password = data['password']

     user = User.query.filter_by(username=username).first()

     if not user or not user.check_password(password):
          abort(401, 'Invalid username or password')

     access_token= create_access_token(identity=username)
     response = make_response(jsonify({'message': 'Login Sucessful'}), 200)

     csrf_token = create_refresh_token(identity=username)
     response.set_cookie('csrf_access_token', csrf_token, httponly=True, secure=False)
     set_access_cookies(response, access_token)
     return response

    
@user_route.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
     response = make_response(jsonify({"message": "Logout successful"}), 200)
     unset_jwt_cookies(response)
     return response

