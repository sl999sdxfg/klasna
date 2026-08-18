from fastapi import status

from .conftest import Endpoints
from .test_helpers import (
    assert_created_matches_input,
    assert_has_valid_id,
)
from .utils import teacher_data


def test_create_teacher(client):
    data = teacher_data()
    response = client.post(Endpoints.TEACHERS, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert_created_matches_input(data, response.json())


def test_teacher_get(client, created_teacher):
    teacher_id = created_teacher["id"]
    get_result = client.get(f"{Endpoints.TEACHERS}{teacher_id}").json()
    assert created_teacher.items() <= get_result.items()
    assert_has_valid_id(get_result)


def test_teacher_get_404(client):
    non_existing_id = 999_999_999
    response = client.get(f"{Endpoints.TEACHERS}{non_existing_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"no Teacher with id={non_existing_id}"


def test_teacher_delete(client, created_teacher):
    url = f"{Endpoints.TEACHERS}{created_teacher['id']}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
