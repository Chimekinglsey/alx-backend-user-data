#!/usr/bin/env python3
"""
9. Basic - User credentials
"""
import base64
import binascii
from .auth import Auth


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
        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)
