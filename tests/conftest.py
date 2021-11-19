import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from widgets.models import Base


@pytest.fixture(name="session")
def session_fixture():
    """in memory sqlite db session"""
    eng = create_engine("sqlite://")

    Base.metadata.bind = eng
    Base.metadata.create_all()

    Session = sessionmaker(bind=eng)
    yield Session
