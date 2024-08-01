#!/usr/bin/env python3
"""Encrypting passwords."""
import bcrypt


def hash_password(password):
    """A function that returns a salted,
    hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password, password):
    """A function that check the password with hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)
