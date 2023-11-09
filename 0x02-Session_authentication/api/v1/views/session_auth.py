#!/usr/bin/env python3
"""
Module for Session Authentication
"""
from models.user import User
from flask import request, Flask, jsonify


app = Flask(__name__)


@app.route('/api/v1/auth_session/login', methods=['POST'],
           strict_slashes=False)
def authenticate():
    """Handles all routes for session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = None
    for _user in users:
        if _user.is_valid_password(password):
            user = _user
    if not user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    s_id = auth.create_session(user)
    cookie_value = auth.session_cookie(request)
    response = jsonify(User.to_json(user))
    response.set_cookie('session_id', str(cookie_value))
    return response

