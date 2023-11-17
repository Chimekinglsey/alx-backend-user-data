#!/usr/bin/env python3
"""End-to-end integration test """
import requests

base_url = 'http://127.0.0.1:5000/'
def register_user(email: str, password: str) -> None:
    data = {"email": email, "password": password}
    """ test register user method"""
    response = requests.post(base_url+'users', data=data)
    assert response.status_code == 200

    assert response.request.url == base_url+'users'
    assert  "email" in response.text


def log_in_wrong_password(email: str, password: str) -> None:
    """ test register user method"""
    data = {"email": email, "password": password}

    response = requests.post(f'{base_url}sessions')
    assert response.status_code == 401
    assert response.request.url == base_url+'sessions'
    assert response.request.method == 'POST'


def log_in(email: str, password: str) -> str:
    """ test register user method"""
    data = {"email": email, "password": password}

    response = requests.get(f'{base_url}profile')
    assert response.status_code == 403
    assert response.request.method == 'GET'
    assert response.request.url == base_url+'profile'

def profile_unlogged() -> None:
    response = requests.get(f'{base_url}')
    assert response.status_code == 200
    assert response.request.method == 'GET'
    assert "Bienvenue" in response.text

def profile_logged(session_id: str) -> None:
    response = requests.post(f'{base_url}sessions')
    assert response.status_code == 401
    assert response.request.method == 'POST'


def log_out(session_id: str) -> None:
    response = requests.delete(f'{base_url}sessions')
    assert response.status_code == 403
    assert response.request.method == 'DELETE'


def reset_password_token(email: str) -> str:
    response = requests.post(f'{base_url}reset_password')
    assert response.status_code == 403
    assert response.request.method == 'POST'

def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {"email": email, "password": new_password,
            "reset_token": reset_token}

    response = requests.put(f'{base_url}reset_password', data=data)
    assert response.status_code == 200
    assert response.request.method == 'PUT'


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
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)