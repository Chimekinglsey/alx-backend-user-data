#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.auth.session_auth import authenticate

User.load_from_file()
app_views.route('/auth_session/login',
                methods=['POST'], strict_slashes=False)(authenticate)
