#!/usr/bin/env python3
"""
Module for Session Authentication
"""
from uuid import uuid4
from .auth import Auth


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
