from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .. import database
from ..database import get_session
from ..main import app
from .test_helpers import JsonDict, json_dict
from .utils import parent_data, student_data, teacher_data


class Endpoints:
    BASE_URL = "http://127.0.0.1:8000"
    STUDENTS = f"{BASE_URL}/students/"
    PARENTS = f"{BASE_URL}/parents/"
    TEACHERS = f"{BASE_URL}/teachers/"


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(autouse=True)
def db_setup() -> Generator[None, None, None]:
    database.engine = test_engine
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


def get_test_session() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def created_student(client: TestClient) -> JsonDict:
    return json_dict(client.post(Endpoints.STUDENTS, json=student_data()))


@pytest.fixture
def created_parent(client: TestClient) -> JsonDict:
    return json_dict(client.post(Endpoints.PARENTS, json=parent_data()))


@pytest.fixture
def created_teacher(client: TestClient) -> JsonDict:
    return json_dict(client.post(Endpoints.TEACHERS, json=teacher_data()))
