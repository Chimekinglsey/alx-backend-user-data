#!/usr/bin/env python3
"""
 10. Basic - User object
"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Simulates Basic REST API Authentication"""
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns Base64 encoded Authorization header """
        if not authorization_header or not (isinstance
                                            (authorization_header, str)):
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """returns decoded value of a Base64 string"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            byte_header = base64_authorization_header.encode('ascii')
            return base64.b64decode(byte_header).decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """retrieve encoded user email and password"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)
    

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return User Instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overload Auth.current_user, retrieves User instance of a request"""
        token = self.authorization_header(request)
        user = None
        if token:
            b64 = self.extract_base64_authorization_header(token)
            b4_decoded = self.decode_base64_authorization_header(b64)
            data = self.extract_user_credentials(b4_decoded)
            user = self.user_object_from_credentials(data[0], data[1])
        return user
