from fastapi import status
from sqlmodel import Session, select

from ..models import Student
from .conftest import Endpoints, test_engine
from .test_helpers import (
    assert_created_matches_input,
    assert_has_valid_id,
    assert_not_found,
)
from .utils import MISSING_ID, student_data


def test_student_creation(client):
    payload = student_data()
    post_result = client.post(Endpoints.STUDENTS, json=payload).json()
    assert_has_valid_id(post_result)
    assert_created_matches_input(payload, post_result)


def test_student_retrieval(client, created_student):
    get_result = client.get(f"{Endpoints.STUDENTS}{created_student['id']}").json()
    assert_created_matches_input(student_data(), get_result)


def test_student_retrieval_404(client):
    assert_not_found(
        client.get(f"{Endpoints.STUDENTS}{MISSING_ID}"), "Student", MISSING_ID
    )


def test_student_delete(client, created_student):
    url = f"{Endpoints.STUDENTS}{created_student['id']}"
    assert client.delete(url).status_code == status.HTTP_200_OK
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND


def test_students_all_retrieval(client):
    response = client.get(Endpoints.STUDENTS)
    assert response.status_code == status.HTTP_200_OK
    with Session(test_engine) as session:
        all_students_in_db = session.exec(select(Student)).all()
    expected = [s.model_dump(mode="json") for s in all_students_in_db]
    assert response.json() == expected


def test_student_update(client, created_student):
    url = f"{Endpoints.STUDENTS}{created_student['id']}"
    updated_student_data = student_data(
        name="Petro", surname="Goloborodko", birthday="2012-01-11"
    )
    post_result = client.patch(url=url, json=updated_student_data).json()
    assert_created_matches_input(updated_student_data, post_result)
