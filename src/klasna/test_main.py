import pytest
from fastapi import status
from fastapi.testclient import TestClient
from .main import app, get_session, Student
from sqlmodel import create_engine, select, Session, SQLModel
from sqlalchemy.pool import StaticPool
from typing import List
from pydantic import TypeAdapter

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_test_session():
    with Session(test_engine) as session:
        yield session


SQLModel.metadata.create_all(test_engine)

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

baseurl = "http://127.0.0.1"
student_endpoint = baseurl + "/students/"


@pytest.fixture
def created_student():
    student_data = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    response = client.post(student_endpoint, json=student_data)
    return response.json()


def test_student_creation():
    student_data = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    post_result: dict = client.post(
        student_endpoint,
        json=student_data,
    ).json()

    assert student_data.items() <= post_result.items()
    assert post_result["id"] is not None
    assert isinstance(post_result["id"], int)
    assert post_result["id"] >= 0


def test_student_get():
    student_data = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    post_result: dict = client.post(
        student_endpoint,
        json=student_data,
    ).json()
    get_result: dict = client.get(f"{student_endpoint}{post_result["id"]}").json()
    assert get_result.items() == post_result.items()
    assert get_result["id"] is not None
    assert isinstance(post_result["id"], int)
    assert get_result["id"] >= 0


def test_student_get_404():
    non_existing_id = 999_999_999
    get_response: dict = client.get(f"{student_endpoint}{non_existing_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    content = f'{{"detail":"no Student with id={non_existing_id}"}}'
    content = content.encode("utf-8")
    assert get_response.content == content


def test_student_delete(created_student):
    url = f"{student_endpoint}{created_student["id"]}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND


def test_student_update(created_student):
    url = f"{student_endpoint}{created_student["id"]}"
    updated_student_data = {
        "name": "Petro",
        "surname": "Goloborodko",
        "birthday": "2012-01-11",
    }
    print("url=", url)
    print(f"id={created_student}")
    response = client.patch(url, json=updated_student_data)
    assert response.status_code == status.HTTP_200_OK
    assert updated_student_data.items() <= response.json().items()
    assert len(response.json().items()) == len(updated_student_data.items()) + 1
    assert response.json()["id"] == created_student["id"]


def test_all_students_get():
    response = client.get(student_endpoint)
    assert response.status_code == status.HTTP_200_OK

    with Session(test_engine) as session:
        all_students_in_db = session.exec(select(Student)).all()

    expected = [s.model_dump(mode="json") for s in all_students_in_db]

    assert response.json() == expected
