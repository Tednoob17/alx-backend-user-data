#!/usr/bin/env python3
"""Session DB Auth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth Class"""

    def create_session(self, user_id=None):
        """Create Session"""
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for Session ID"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        user_session = user_session[0]
        expired_time = user_session.created_at + timedelta(
            seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy Session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
