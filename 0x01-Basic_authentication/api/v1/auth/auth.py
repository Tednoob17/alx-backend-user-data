#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for i in excluded_paths:
            if i[-1] == '*':
                if path.startswith(i[:-1]):
                    return False
            elif path == i:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.he
    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
