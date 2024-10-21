#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from typing import Any

from werkzeug import Response

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, redirect
from flasgger.utils import swag_from
from Controllers.AuthController import AuthController
@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    -- This can be access only by Admin
    """

    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

@app_views.route('/users/Register', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/Register.yml', methods=['PUT'])
def Register():
    """ Register a new user
    """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    username  = data.get('username')
    email = data.get('email')
    password = data.get('password')
    admin = data.get('admin')

    try:
        AuthController.register_user(username, email, password, admin)
        return jsonify({"username": username, "email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app_views.route('/users/login', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/login.yml', methods=['POST'])
def login() -> tuple[Any, int] | Any:
    """
    - POST login user
    """
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    email = data.get("email")
    password = data.get("password")
    if not AuthController.valid_login(email, password):
        abort(401)
    session_id = AuthController.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app_views.route('/users/logout', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/logout.yml', methods=['DELETE'])
def logout() -> Response:
    """
    - logout user
    """
    session_id = request.cookies.get("session_id")
    user = AuthController.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AuthController.destroy_session(user.id)
    return redirect("/")