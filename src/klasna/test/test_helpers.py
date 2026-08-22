from fastapi import status


def assert_has_valid_id(entity: dict) -> None:
    """Assert entity has a valid auto-generated id."""
    assert "id" in entity
    assert isinstance(entity["id"], int)
    assert entity["id"] > 0


def assert_created_matches_input(input_data: dict, created: dict) -> None:
    """Assert every field sent in input_data made it into the created entity, plus a valid id."""
    assert input_data.items() <= created.items()
    assert_has_valid_id(created)


def assert_not_found(response, model_name: str, entity_id: int) -> None:
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"no {model_name} with id={entity_id}"
