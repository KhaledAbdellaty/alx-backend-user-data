#!/usr/bin/env python3
"""
A SessionAuth Module.
"""
from .auth import Auth
from uuid import uuid4


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
