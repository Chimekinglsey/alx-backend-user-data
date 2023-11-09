#!/usr/bin/env python3
"""
Module for Session Authentication
"""
from uuid import uuid4
from .auth import Auth
from models.user import User
from flask import request, Flask, jsonify, abort


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


class SessionAuth(Auth):
    """Creates new authentication mechanism"""
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id and isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User_id based on a session_id"""
        if session_id and isinstance(session_id, str):
            user_id = self.user_id_by_session_id.get(session_id)
            return user_id
        return None

    def current_user(self, request=None) -> str:
        """Overload that returns a user instance based on cookie value"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)
