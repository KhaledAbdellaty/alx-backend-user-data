#!/usr/bin/env python3
"""
Template for all authentication system
"""
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    """
    This class is the template for all authentication system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        A function that returns True if the path is
        not in the list of strings excluded_paths.
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """A function that returns None"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that returns the current user"""
        return None

    def session_cookie(self, request=None):
        """A function that returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
