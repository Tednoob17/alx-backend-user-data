#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if login is valid"""
        try:
            user_found = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              user_found.hashed_password)

    def create_session(self, email: str):
        """Creates a session ID"""
        try:
            user_found = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_found.id, session_id=session_id)
        return session_id

        user_found = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user_found

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get Reset Password token"""
        try:
            user_found = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user_found.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password"""
        if reset_token is None or password is None:
            return None
        try:
            user_found = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_password = _hash_password(password)
        self._db.update_user(user_found.id,
                             hashed_password=hashed_password,
                             reset_token=None)
