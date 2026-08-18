def assert_has_valid_id(entity: dict) -> None:
    """Assert entity has a valid auto-generated id."""
    assert "id" in entity
    assert isinstance(entity["id"], int)
    assert entity["id"] > 0


def assert_created_matches_input(input_data: dict, created: dict) -> None:
    """Assert every field sent in input_data made it into the created entity, plus a valid id."""
    assert input_data.items() <= created.items()
    assert_has_valid_id(created)
