import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.tags import Tag
from app.database import Base

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

def test_create_tag(session):
    tag = Tag(name="Roman", description="Roman classique")
    session.add(tag)
    session.commit()
    assert tag.id is not None
    assert tag.name == "Roman"
    assert tag.description == "Roman classique"
