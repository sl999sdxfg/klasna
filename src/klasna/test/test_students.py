from fastapi import status
from sqlmodel import Session, select

from ..models import Student
from .conftest import Endpoints, test_engine
from .test_helpers import (
    assert_created_matches_input,
    assert_has_valid_id,
)
from .utils import student_data


def test_student_creation(client):
    student_data_ = student_data()
    post_result = client.post(
        Endpoints.STUDENTS,
        json=student_data_,
    ).json()
    assert_has_valid_id(post_result)
    assert_created_matches_input(student_data_, post_result)


def test_student_retreival(client, created_student):
    get_result = client.post(Endpoints.STUDENTS, json=created_student).json()
    no_id = {k: v for k, v in created_student.items() if k != "id"}
    assert_created_matches_input(no_id, get_result)


def test_student_retreival_404(client):
    non_existing_id = 999_999_999
    get_response = client.get(f"{Endpoints.STUDENTS}{non_existing_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()["detail"] == f"no Student with id={non_existing_id}"


def test_student_delete(client, created_student):
    url = f"{Endpoints.STUDENTS}{created_student['id']}"
    assert client.delete(url).status_code == status.HTTP_200_OK
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND


def test_students_all_retreival(client):
    response = client.get(Endpoints.STUDENTS)
    assert response.status_code == status.HTTP_200_OK
    with Session(test_engine) as session:
        all_students_in_db = session.exec(select(Student)).all()
    expected = [s.model_dump(mode="json") for s in all_students_in_db]
    assert response.json() == expected


def test_student_update(client, created_student):
    url = f"{Endpoints.STUDENTS}{created_student['id']}"
    updated_student_data = {
        "name": "Petro",
        "surname": "Goloborodko",
        "birthday": "2012-01-11",
    }
    post_result = client.patch(url=url, json=updated_student_data).json()
    assert_created_matches_input(updated_student_data, post_result)
