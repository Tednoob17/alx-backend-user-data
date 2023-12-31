#!/usr/bin/env python3
""" Main Module """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
import requests


def register_user(email: str, password: str) -> None:
    """register user"""
    return requests.post('http://localhost:5000/users', data={
        'email': email,
        'password': password
    })


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    return requests.post('http://localhost:5000/sessions', data={
        'email': email,
        'password': password
    })


def log_in(email: str, password: str) -> str:
    """log in"""
    response = requests.post('http://localhost:5000/sessions', data={
        'email': email,
        'password': password
    })
    return response.cookies.get('session_id')



def profile_logged(session_id: str) -> None:
    """profile logged"""
    return requests.get('http://localhost:5000/profile', cookies={
        'session_id': session_id
    })


def log_out(session_id: str) -> None:
    """log out"""
    return requests.delete('http://localhost:5000/sessions', cookies={
        'session_id': session_id
    })


def reset_password_token(email: str) -> str:
    """reset password token"""
    return requests.post('http://localhost:5000/reset_password', data={
        'email': email
    })


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password"""
    return requests.put('http://localhost:5000/reset_password', data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)

    log_in(EMAIL, NEW_PASSWD)
