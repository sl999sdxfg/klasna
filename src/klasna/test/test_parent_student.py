from fastapi import status

from .conftest import Endpoints
from .utils import MISSING_ID


def _link_url(student_id, parent_id):
    return f"{Endpoints.STUDENTS}{student_id}/parents/{parent_id}"


def test_student_parent_link(client, created_student, created_parent):
    post_response = client.post(_link_url(created_student["id"], created_parent["id"]))
    assert post_response.status_code == status.HTTP_200_OK
    assert created_parent in post_response.json()["parents"]


def test_student_parent_unlink(client, created_student, created_parent):
    student_id = created_student["id"]
    parent_id = created_parent["id"]
    post_response = client.post(_link_url(student_id, parent_id))
    assert post_response.status_code == status.HTTP_200_OK
    assert created_parent in post_response.json()["parents"]

    delete_response = client.delete(_link_url(student_id, parent_id))
    get_response = client.get(f"{Endpoints.STUDENTS}{student_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    assert created_parent not in get_response.json()["parents"]


def test_student_parent_unlink_409(client, created_student, created_parent):
    student_id = created_student["id"]
    parent_id = created_parent["id"]
    delete_response = client.delete(_link_url(student_id, parent_id))
    get_response = client.get(f"{Endpoints.STUDENTS}{student_id}")
    assert delete_response.status_code == status.HTTP_409_CONFLICT
    assert created_parent not in get_response.json()["parents"]


def test_student_parent_unlink_404(client, created_student, created_parent):
    student_id = created_student["id"]
    parent_id = created_parent["id"]
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
