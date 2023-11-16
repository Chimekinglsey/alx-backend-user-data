#!usr/bin/env python3
""" User Authentication Module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypt password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
