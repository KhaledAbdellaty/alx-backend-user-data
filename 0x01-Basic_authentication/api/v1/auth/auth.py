#!/usr/bin/env python3
"""
Template for all authentication system
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class is the template for all authentication system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        A function that returns True if the path is
        not in the list of strings excluded_paths.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        else:
            for excluded_path in excluded_paths:
                if path == excluded_path[0:-1] or path in excluded_paths:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """A function that returns None"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that returns None"""
        return None
