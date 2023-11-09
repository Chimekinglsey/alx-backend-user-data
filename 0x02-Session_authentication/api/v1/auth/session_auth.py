#!/usr/bin/env python3
"""
Module for Session Authentication
"""
from uuid import uuid4
from .auth import Auth
from models.user import User


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
