#!/usr/bin/env python3
"""Session Authentication"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User
from datetime import datetime, timedelta


class SessionAuth(Auth):
    """Session Authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session for the user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user_id by session_id"""
        if session_id is None:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        created_at = session.get('created_at')
        if created_at is None:
            return None
        session_duration = self.session_duration
        if session_duration <= 0:
            return session.get('user_id')
        now = datetime.now()
        if created_at + timedelta(seconds=session_duration) < now:
            del self.user_id_by_session_id[session_id]
            return None
        return session.get('user_id')

    def current_user(self, request=None):
        """Return current user"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy(self, request=None):
        """Destroy session"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True

    def destroy_session(self, request=None):
        """Destroy session"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
