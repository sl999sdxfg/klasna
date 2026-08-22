from collections.abc import Mapping
from typing import Protocol, cast

from fastapi import status

JsonDict = dict[str, object]
JsonMapping = Mapping[str, object]


class HttpResponse(Protocol):
    status_code: int

    def json(self) -> object: ...


def json_object(response: HttpResponse) -> object:
    return response.json()


def json_dict(response: HttpResponse) -> JsonDict:
    payload = json_object(response)
    assert isinstance(payload, dict)
    return cast(JsonDict, payload)


def entity_id(entity: JsonDict) -> int:
    value = entity["id"]
    assert isinstance(value, int)
    return value


def assert_has_valid_id(entity: JsonDict) -> None:
    """Assert entity has a valid auto-generated id."""
    assert entity_id(entity) > 0


def assert_created_matches_input(input_data: JsonMapping, created: JsonDict) -> None:
    """Assert input fields are present on the created entity, plus a valid id."""
    assert input_data.items() <= created.items()
    assert_has_valid_id(created)


def assert_not_found(response: HttpResponse, model_name: str, missing_id: int) -> None:
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json_dict(response)["detail"] == f"no {model_name} with id={missing_id}"
