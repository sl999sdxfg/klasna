from fastapi import status

from .conftest import Endpoints


def test_student_parent_link(client, created_student, created_parent):
    student_id = created_student["id"]
    parent_id = created_parent["id"]
    post_response = client.post(f"{Endpoints.STUDENTS}{student_id}/parents/{parent_id}")
    assert post_response.status_code == status.HTTP_200_OK
    assert created_parent in post_response.json()["parents"]


def test_student_parent_unlink(client, created_student, created_parent):
    student_id = created_student["id"]
    parent_id = created_parent["id"]
    post_response = client.post(f"{Endpoints.STUDENTS}{student_id}/parents/{parent_id}")
    assert post_response.status_code == status.HTTP_200_OK
    assert created_parent in post_response.json()["parents"]
    delete_response = client.delete(
        f"{Endpoints.STUDENTS}{student_id}/parents/{parent_id}"
    )

    get_response = client.get(f"{Endpoints.STUDENTS}{student_id}")
    assert delete_response.status_code == status.HTTP_200_OK
    assert created_parent not in get_response.json()["parents"]
    delete_response = client.delete(
        f"{Endpoints.STUDENTS}{student_id}/parents/{parent_id}"
    )
    get_response = client.get(f"{Endpoints.STUDENTS}{student_id}")
    assert delete_response.status_code == status.HTTP_409_CONFLICT
    assert created_parent not in get_response.json()["parents"]
    delete_response = client.delete(
        f"{Endpoints.STUDENTS}{student_id}/parents/{999_999_999}"
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND

    delete_response = client.delete(
        f"{Endpoints.STUDENTS}{999_999_999}/parents/{parent_id}"
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND

    delete_response = client.delete(
        f"{Endpoints.STUDENTS}{999_999_999}/parents/{999_999_999}"
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
