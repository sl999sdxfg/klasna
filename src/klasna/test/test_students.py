from typing import cast

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from ..models import Student
from .conftest import Endpoints, test_engine
from .test_helpers import (
    JsonDict,
    assert_created_matches_input,
    assert_has_valid_id,
    assert_not_found,
    entity_id,
    json_dict,
    json_object,
)
from .utils import MISSING_ID, student_data


def test_student_creation(client: TestClient) -> None:
    payload = student_data()
    post_result = json_dict(client.post(Endpoints.STUDENTS, json=payload))
    assert_has_valid_id(post_result)
    assert_created_matches_input(payload, post_result)


def test_student_retrieval(client: TestClient, created_student: JsonDict) -> None:
    get_result = json_dict(
        client.get(f"{Endpoints.STUDENTS}{entity_id(created_student)}")
    )
    assert_created_matches_input(student_data(), get_result)


def test_student_retrieval_404(client: TestClient) -> None:
    assert_not_found(
        client.get(f"{Endpoints.STUDENTS}{MISSING_ID}"), "Student", MISSING_ID
    )


def test_student_delete(client: TestClient, created_student: JsonDict) -> None:
    url = f"{Endpoints.STUDENTS}{entity_id(created_student)}"
    assert client.delete(url).status_code == status.HTTP_200_OK
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND


def test_students_all_retrieval(client: TestClient) -> None:
    response = client.get(Endpoints.STUDENTS)
    assert response.status_code == status.HTTP_200_OK
    with Session(test_engine) as session:
        all_students_in_db = session.exec(select(Student)).all()
    expected = [cast(object, s.model_dump(mode="json")) for s in all_students_in_db]
    assert json_object(response) == expected


def test_student_update(client: TestClient, created_student: JsonDict) -> None:
    url = f"{Endpoints.STUDENTS}{entity_id(created_student)}"
    updated_student_data = student_data(
        name="Petro", surname="Goloborodko", birthday="2012-01-11"
    )
    post_result = json_dict(client.patch(url=url, json=updated_student_data))
    assert_created_matches_input(updated_student_data, post_result)
