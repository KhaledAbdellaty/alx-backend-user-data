#!/usr/bin/env python3
"""
BasicAuth Module.
"""
from .auth import Auth
import re
import base64


class BasicAuth(Auth):
    """
    A class that inherits from Auth.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """A function that returns the Base64 part of
        the Authorization header for a Basic Authentication.
        """
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """A function that returns the decoded value
        of a Base64 string
        """
        if isinstance(base64_authorization_header, str):
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                )
                return res.decode('utf-8')
            except UnicodeDecodeError:
                return None
