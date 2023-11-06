#!/usr/bin/env python3
"""Module for User Authentication Management"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages API authentication"""
    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false, determine if authentication is needed"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None, will implement http request header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None, will authenticate current user"""
        return None
