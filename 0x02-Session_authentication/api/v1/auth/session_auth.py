#!/usr/bin/env python3
"""
A SessionAuth Module.
"""
from .auth import Auth
from uuid import uuid4
from views.users import User


class SessionAuth(Auth):
    """
    A SessionAuth class that inherits from Auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        A function that creates a Session ID for a user.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        A function that returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        A function at returns a User instance based on a cookie value.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user
