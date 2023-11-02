#!/usr/bin/env python3
"""Module for User object view"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from typing import Tuple
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handle_login() -> Tuple[str, int]:
    """GET /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    email, password = request.form.get('email'), request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
