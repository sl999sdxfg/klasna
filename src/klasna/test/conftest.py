import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .. import database
from ..database import get_session
from ..main import app


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
def db_setup():
    database.engine = test_engine
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


def get_test_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def created_student(client):
    student_data = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    post_result = client.post(Endpoints.STUDENTS, json=student_data)
    return post_result.json()


@pytest.fixture
def created_parent(client):
    parent_data = {
        "name": "Stepan",
        "surname": "Bratkovskyi",
        "birthday": "1991-03-04",
        "phone": "+380975840179",
        "email": "stepanbb@gmail.com",
    }
    post_result = client.post(Endpoints.PARENTS, json=parent_data)
    return post_result.json()


@pytest.fixture
def created_teacher(client):
    teacher_data = {
        "name": "Panas",
        "surname": "Semerchenko",
        "birthday": "1988-08-14",
        "phone": "+380773147189",
        "email": "panassem@gmail.com",
        "subjects": "history",
        "classes": "6,7,8",
    }
    post_result = client.post(Endpoints.TEACHERS, json=teacher_data)
    print(">>>> post_resust= ", post_result)
    return post_result.json()
