#!/usr/bin/env python3
"""
6. Simulated Basic Authentication
"""
import base64
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
