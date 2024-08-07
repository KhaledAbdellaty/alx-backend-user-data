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
        """A function that returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """A function that returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that returns None"""
        return None
