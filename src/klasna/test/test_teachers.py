from fastapi import status
from fastapi.testclient import TestClient

from .conftest import Endpoints
from .test_helpers import (
    JsonDict,
    assert_created_matches_input,
    assert_has_valid_id,
    assert_not_found,
    entity_id,
    json_dict,
)
from .utils import MISSING_ID, teacher_data


def test_create_teacher(client: TestClient) -> None:
    data = teacher_data()
    response = client.post(Endpoints.TEACHERS, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert_created_matches_input(data, json_dict(response))


def test_teacher_get(client: TestClient, created_teacher: JsonDict) -> None:
    get_result = json_dict(
        client.get(f"{Endpoints.TEACHERS}{entity_id(created_teacher)}")
    )
    assert created_teacher.items() <= get_result.items()
    assert_has_valid_id(get_result)


def test_teacher_get_404(client: TestClient) -> None:
    assert_not_found(
        client.get(f"{Endpoints.TEACHERS}{MISSING_ID}"), "Teacher", MISSING_ID
    )


def test_teacher_delete(client: TestClient, created_teacher: JsonDict) -> None:
    url = f"{Endpoints.TEACHERS}{entity_id(created_teacher)}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
