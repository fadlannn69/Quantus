import pytest
from fastapi.testclient import TestClient
from apk.main import app
from apk.database.session import get_session
from sqlmodel import Session

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture
def session():
    with Session(get_session()) as s:
        yield s
