import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.users import User, UserRole
from app.database import Base
from datetime import datetime

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()

def test_create_user(session):
    user = User(username="alice", email="alice@example.com", password="hashedpwd", role=UserRole.USER.value)
    session.add(user)
    session.commit()
    assert user.id is not None
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.role == UserRole.USER.value
    assert isinstance(user.date_created, datetime)

def test_user_role_enum():
    assert UserRole.USER.value == "user"
    assert UserRole.MODERATOR.value == "moderator"
    assert UserRole.ADMIN.value == "admin"
