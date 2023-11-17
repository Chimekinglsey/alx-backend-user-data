#!/usr/bin/env python3
""" Flask Authentication App"""
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Welcome page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Create a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        if AUTH._db.find_user_by(email=email):
            return jsonify({"message": "email already registered"}), 400
    except NoResultFound:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Create a Session ID for a logged in user"""
    email, password = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email, password):
        Session_ID = AUTH.create_session(email=email)
        response = make_response(jsonify
                                 ({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', Session_ID)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        abort(403)
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Send reset password token to email"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        token = None
    if token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
