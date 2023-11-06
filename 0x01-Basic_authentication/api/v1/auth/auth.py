#!/usr/bin/env python3
"""Module for User Authentication Management"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages API authentication"""
    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) < 1:
            return True
        if not path.endswith('/'):
            path = path + '/'
        for route in excluded_paths:
            if not route.endswith('/'):
                route = route + '/'
        return False if path in excluded_paths else True
    
    def authorization_header(self, request=None) -> str:
        """Returns None, will implement http request header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None, will authenticate current user"""
        return None
