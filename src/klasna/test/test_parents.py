from fastapi import status

from .conftest import Endpoints
from .test_helpers import assert_created_matches_input, assert_not_found
from .utils import MISSING_ID, parent_data


def test_parent_creation(client):
    payload = parent_data()
    post_result = client.post(Endpoints.PARENTS, json=payload).json()
    assert_created_matches_input(payload, post_result)


def test_parent_get(client, created_parent):
    get_result = client.get(f"{Endpoints.PARENTS}{created_parent['id']}").json()
    assert_created_matches_input(parent_data(), get_result)


def test_parent_get_404(client):
    assert_not_found(
        client.get(f"{Endpoints.PARENTS}{MISSING_ID}"), "Parent", MISSING_ID
    )


def test_parent_delete(client, created_parent):
    url = f"{Endpoints.PARENTS}{created_parent['id']}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
