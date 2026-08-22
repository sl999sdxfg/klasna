from fastapi import status

from .conftest import Endpoints
from .test_helpers import (
    assert_created_matches_input,
    assert_has_valid_id,
    assert_not_found,
)
from .utils import MISSING_ID, teacher_data


def test_create_teacher(client):
    data = teacher_data()
    response = client.post(Endpoints.TEACHERS, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert_created_matches_input(data, response.json())


def test_teacher_get(client, created_teacher):
    get_result = client.get(f"{Endpoints.TEACHERS}{created_teacher['id']}").json()
    assert created_teacher.items() <= get_result.items()
    assert_has_valid_id(get_result)


def test_teacher_get_404(client):
    assert_not_found(
        client.get(f"{Endpoints.TEACHERS}{MISSING_ID}"), "Teacher", MISSING_ID
    )


def test_teacher_delete(client, created_teacher):
    url = f"{Endpoints.TEACHERS}{created_teacher['id']}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
