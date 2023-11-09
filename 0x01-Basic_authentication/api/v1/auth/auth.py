#!/usr/bin/env python3
"""Module for User Authentication Management"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """Manages API authentication"""
    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

        # if path is None or excluded_paths is None or len(excluded_paths) < 1:
        #     return True

        # if not path.endswith('/'):
        #     path = path + '/'

        # for route in excluded_paths:
        #     if not route.endswith('/'):
        #         route = route + '/'
        #     if route.endswith('*'):
        #         route = route.rstrip('*')
        #         if path.startswith(route):
        #             return True
        #     else:
        #         if path == route:
        #             return True
        # return path in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Request validation"""
        if request is not None:
            return (request.headers.get('Authorization', None))
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None, will authenticate current user"""
        return None
