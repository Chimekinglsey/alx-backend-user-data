#!/usr/bin/env python3
""" User Authentication Module
"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB, User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Encrypt password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate unique user id"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user to the database"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """validate user credential for login"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Returns created Session ID"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user.session_id = _generate_uuid()
                self._db._session.add(user)
                self._db._session.commit()
                return user.session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> None:
        """Fetches user-data from session_id"""
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Terminate a user's session"""
        user = self._db.find_user_by(id=user_id)
        if user:
            user.session_id = None
            self._db._session.add(user)
            self._db._session.commit()

    def get_reset_password_token(self, email: str) -> str:
        """Send reset password token to email"""
        user = self._db.find_user_by(email=email)
        if user:
            self._db.update_user(user.id, reset_token=_generate_uuid())
            # user.reset_token = _generate_uuid()
            return user.reset_token
        return ValueError
