from fastapi import status

from .conftest import Endpoints
from .test_helpers import (
    assert_created_matches_input,
    assert_has_valid_id,
)
from .utils import parent_data


def test_parent_creation(client):
    parent_data_ = parent_data()
    post_result = client.post(Endpoints.PARENTS, json=parent_data_).json()
    assert_created_matches_input(parent_data_, post_result)


def test_parent_get(client):
    parent_data_ = parent_data()
    post_result: dict = client.post(
        Endpoints.PARENTS,
        json=parent_data_,
    ).json()
    get_result: dict = client.get(f"{Endpoints.PARENTS}{post_result['id']}").json()
    assert post_result.items() <= get_result.items()
    assert get_result["students"] == []
    assert_has_valid_id(post_result)


def test_parent_get_404(client):
    non_existing_id = 999_999_999
    get_response: dict = client.get(f"{Endpoints.PARENTS}{non_existing_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    content = f'{{"detail":"no Parent with id={non_existing_id}"}}'
    content = content.encode("utf-8")
    assert get_response.content == content


def test_parent_delete(client, created_parent):
    url = f"{Endpoints.PARENTS}{created_parent['id']}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
