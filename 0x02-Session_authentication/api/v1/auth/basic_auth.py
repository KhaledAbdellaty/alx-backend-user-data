#!/usr/bin/env python3
"""
BasicAuth Module.
"""
from .auth import Auth
import re
import base64
from typing import Tuple, TypeVar
from models.user import User


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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """A finction that returns the user email and
        passowrd from the Base64 decoded value
        """
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            re_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip()
            )
            if re_match:
                user = re_match.group('user')
                password = re_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        A function that returns the User instance
        based on his email and password
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            users = User.search({'email': user_email})
            if len(users) > 0:
                if users[0].is_valid_password(user_pwd):
                    return users[0]
                else:
                    return None
            else:
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that retrieves the User from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
