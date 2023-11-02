#!/usr/bin/env python3
"""SessionExpAuth module"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        """Initialize SessionExpAuth"""
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """Create a Session ID for a user_id"""
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Return a User ID based on a Session ID"""
        if session_id is None:
            return None
        user_infos = self.user_id_by_session_id.get(session_id)
        if user_infos is None:
            return None
        if "created_at" not in user_infos.keys():
            return None
        if self.session_duration <= 0:
            return user_infos.get("user_id")
        created_at = user_infos.get("created_at")
        duration = created_at + timedelta(seconds=self.session_duration)
        if duration < datetime.now():
            return None
        return user_infos.get("user_id")
