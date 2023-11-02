#!/usr/bin/env python3
"""User Session Model"""
from .base import Base


class UserSession(Base):
    """User Session Model"""

    def __init__(self, *args: list, **kwargs: dict):
        """initializes user session"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.session_id = kwargs.get('session_id', "")
