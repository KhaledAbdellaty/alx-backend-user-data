#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """A function that hashes a password"""
    return bcrypt.hashpw(password=password.encode('utf-8'),
                         salt=bcrypt.gensalt())


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
        user = self._db.find_user_by(email=email)
        print(user)
        if  user is None:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")
