from fastapi import status

from .conftest import Endpoints
from .utils import sample_teacher


def test_create_teacher(client):
    teacher_data = sample_teacher()
    post_response = client.post(Endpoints.TEACHERS, json=teacher_data)
    assert post_response.status_code == status.HTTP_200_OK
    assert teacher_data.items() <= post_response.json().items()
    assert post_response.json()["id"] is not None
    assert isinstance(post_response.json()["id"], int)
    assert post_response.json()["id"] > 0


def test_teacher_get(client, created_teacher):
    teacher_id = created_teacher["id"]
    get_result: dict = client.get(f"{Endpoints.TEACHERS}{teacher_id}").json()
    assert created_teacher.items() <= get_result.items()
    assert get_result["id"] is not None
    assert isinstance(get_result["id"], int)
    assert get_result["id"] >= 0


def test_teacher_get_404(client):
    non_existing_id = 999_999_999
    get_response: dict = client.get(f"{Endpoints.TEACHERS}{non_existing_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    content = f'{{"detail":"no Teacher with id={non_existing_id}"}}'
    content = content.encode("utf-8")
    assert get_response.content == content


def test_teacher_delete(client, created_teacher):
    url = f"{Endpoints.TEACHERS}{created_teacher['id']}"
    client.delete(url)
    assert client.get(url).status_code == status.HTTP_404_NOT_FOUND
