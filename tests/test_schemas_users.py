import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas.users import CreateUser, UpdateUser, UserLogin, Token, UserResponse, UserRole
from datetime import datetime

def test_createuser_schema():
    data = {"username": "bob", "email": "bob@example.com", "password": "pwd", "role": "user"}
    user = CreateUser(**data)
    assert user.username == "bob"
    assert user.email == "bob@example.com"
    assert user.password == "pwd"
    assert user.role == "user"

def test_updateuser_schema():
    data = {"username": None, "email": "maj@example.com", "password": None}
    user = UpdateUser(**data)
    assert user.username is None
    assert user.email == "maj@example.com"
    assert user.password is None

def test_userlogin_schema():
    data = {"email": "bob@example.com", "password": "pwd"}
    login = UserLogin(**data)
    assert login.email == "bob@example.com"
    assert login.password == "pwd"

def test_token_schema():
    data = {"access_token": "abc", "token_type": "bearer"}
    token = Token(**data)
    assert token.access_token == "abc"
    assert token.token_type == "bearer"

def test_userresponse_schema():
    data = {"id": 1, "username": "bob", "email": "bob@example.com", "role": UserRole.USER, "date_created": datetime.utcnow()}
    user = UserResponse(**data)
    assert user.id == 1
    assert user.username == "bob"
    assert user.email == "bob@example.com"
    assert user.role == UserRole.USER
    assert isinstance(user.date_created, datetime)
