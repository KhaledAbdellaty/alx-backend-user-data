#!/usr/bin/env python3
"""Auth module"""
import bcrypt


def _hash_password(password: str):
    """A function that hashes a password"""
    return bcrypt.hashpw(password=password.encode('utf-8'),
                         salt=bcrypt.gensalt())
