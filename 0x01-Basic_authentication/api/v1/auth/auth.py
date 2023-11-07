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
            if route.endswith('*'):
                route = route.rstrip('*')
                if path.startswith(route):
                    return True
            else:
                if path == route:
                    return True
        return False

    def authorization_header(self, request=None) -> str:
        """Request validation"""
        if request is None:
            return None
        elif not (request.headers.get('Authorization')):
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None, will authenticate current user"""
        return None
