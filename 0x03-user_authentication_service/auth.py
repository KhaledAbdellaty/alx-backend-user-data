#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """A function that hashes a password"""
    return bcrypt.hashpw(password=password.encode('utf-8'),
                         salt=bcrypt.gensalt())


def _generate_uuid() -> str:
    """A function that returns
    a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """The Init function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        A function that register new user.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        A function that check the password,
        If it matches return True. In any other case, return False.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'),
            user.hashed_password,
        )

    def create_session(self, email: str) -> str:
        """
        A function that retuens the session ID as a String.
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return
