from fastapi import status
from sqlmodel import Session, select

from ..models import Student
from .conftest import Endpoints, test_engine
from .utils import check_identical_except_id, sample_student


def test_student_creation(client):
    student_data = sample_student()
    post_result = client.post(
        Endpoints.STUDENTS,
        json=student_data,
    ).json()
    check_identical_except_id(student_no_id=student_data, student_with_id=post_result)


def test_student_retreival(client, created_student):
    get_result = client.post(Endpoints.STUDENTS, json=created_student).json()
    no_id = {k: v for k, v in created_student.items() if k != "id"}
    check_identical_except_id(student_no_id=no_id, student_with_id=get_result)


def test_student_retreival_404(client):
    non_existing_id = 999_999_999
    get_response = client.get(f"{Endpoints.STUDENTS}{non_existing_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    content = f'{{"detail":"no Student with id={non_existing_id}"}}'.encode()
    assert get_response.content == content


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
    check_identical_except_id(
        student_no_id=updated_student_data, student_with_id=post_result
    )
