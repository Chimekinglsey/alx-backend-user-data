#!/usr/bin/env python3
"""
Module for Session Authentication
"""
import os
from models.user import User
from api.v1.views import app_views
from typing import Tuple
from flask import request, jsonify, abort


@app_views.route('/api/v1/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def authenticate() -> str:
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
    auth.create_session(user)
    cookie_value = auth.session_cookie(request)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv("SESSION_NAME"), str(cookie_value))
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
