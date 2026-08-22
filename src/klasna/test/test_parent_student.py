from fastapi import status
from fastapi.testclient import TestClient

from .conftest import Endpoints
from .test_helpers import JsonDict, entity_id, json_dict
from .utils import MISSING_ID


def _link_url(student_id: int, parent_id: int) -> str:
    return f"{Endpoints.STUDENTS}{student_id}/parents/{parent_id}"


def test_student_parent_link(
    client: TestClient, created_student: JsonDict, created_parent: JsonDict
) -> None:
    post_response = client.post(
        _link_url(entity_id(created_student), entity_id(created_parent))
    )
    assert post_response.status_code == status.HTTP_200_OK
    parents = json_dict(post_response)["parents"]
    assert isinstance(parents, list)
    assert created_parent in parents


def test_student_parent_unlink(
    client: TestClient, created_student: JsonDict, created_parent: JsonDict
) -> None:
    student_id = entity_id(created_student)
    parent_id = entity_id(created_parent)
    post_response = client.post(_link_url(student_id, parent_id))
    assert post_response.status_code == status.HTTP_200_OK
    linked_parents = json_dict(post_response)["parents"]
    assert isinstance(linked_parents, list)
    assert created_parent in linked_parents

    delete_response = client.delete(_link_url(student_id, parent_id))
    get_response = client.get(f"{Endpoints.STUDENTS}{student_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    remaining_parents = json_dict(get_response)["parents"]
    assert isinstance(remaining_parents, list)
    assert created_parent not in remaining_parents


def test_student_parent_unlink_409(
    client: TestClient, created_student: JsonDict, created_parent: JsonDict
) -> None:
    student_id = entity_id(created_student)
    parent_id = entity_id(created_parent)
    delete_response = client.delete(_link_url(student_id, parent_id))
    get_response = client.get(f"{Endpoints.STUDENTS}{student_id}")
    assert delete_response.status_code == status.HTTP_409_CONFLICT
    remaining_parents = json_dict(get_response)["parents"]
    assert isinstance(remaining_parents, list)
    assert created_parent not in remaining_parents


def test_student_parent_unlink_404(
    client: TestClient, created_student: JsonDict, created_parent: JsonDict
) -> None:
    student_id = entity_id(created_student)
    parent_id = entity_id(created_parent)
    assert (
        client.delete(_link_url(student_id, MISSING_ID)).status_code
        == status.HTTP_404_NOT_FOUND
    )
    assert (
        client.delete(_link_url(MISSING_ID, parent_id)).status_code
        == status.HTTP_404_NOT_FOUND
    )
    assert (
        client.delete(_link_url(MISSING_ID, MISSING_ID)).status_code
        == status.HTTP_404_NOT_FOUND
    )
