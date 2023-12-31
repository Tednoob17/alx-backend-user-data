#!/usr/bin/env python3
"""Basic Authentication"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract Base 64 from header """
        if authorization_header is None or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode Base64"""
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header)
            return base64_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decode_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract User Credentials"""
        if decode_base64_authorization_header is None or \
           not isinstance(decode_base64_authorization_header, str):
            return (None, None)
        try:
            return tuple(decode_base64_authorization_header.split(':', 1))
        except Exception:
            return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """User Object from Credentials"""
        if user_email is None or \
           not isinstance(user_email, str) or \
           user_pwd is None or \
           not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or len(users) == 0:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

   
