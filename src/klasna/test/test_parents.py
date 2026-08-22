from fastapi import status
from fastapi.testclient import TestClient

from .conftest import Endpoints
from .test_helpers import (
    JsonDict,
    assert_created_matches_input,
    assert_not_found,
    entity_id,
    json_dict,
)
from .utils import MISSING_ID, parent_data


def test_parent_creation(client: TestClient) -> None:
    payload = parent_data()
    post_result = json_dict(client.post(Endpoints.PARENTS, json=payload))
    assert_created_matches_input(payload, post_result)


def test_parent_get(client: TestClient, created_parent: JsonDict) -> None:
    get_result = json_dict(
        client.get(f"{Endpoints.PARENTS}{entity_id(created_parent)}")
    )
    assert_created_matches_input(parent_data(), get_result)


def test_parent_get_404(client: TestClient) -> None:
    assert_not_found(
        client.get(f"{Endpoints.PARENTS}{MISSING_ID}"), "Parent", MISSING_ID
    )


def test_parent_delete(client: TestClient, created_parent: JsonDict) -> None:
    url = f"{Endpoints.PARENTS}{entity_id(created_parent)}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
