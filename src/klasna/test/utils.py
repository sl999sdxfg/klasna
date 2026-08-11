def check_identical_except_id(*args, **kwargs):
    """Utility assertion used by tests.

    Usage:
    - check_identical_except_id(entity): assert `id` exists and is an int > 0
    - check_identical_except_id(entity_no_id, entity_with_id): assert that
      items from the no-id entity are present in the with-id entity, and that
      the with-id entity has a valid `id`.
    """
    optional_keys = {"class_id", "students", "subjects", "classes", "phone", "email"}
    # support legacy keyword usage: student_no_id, student_with_id
    if "student_no_id" in kwargs and "student_with_id" in kwargs:
        no_id = kwargs["student_no_id"]
        with_id = kwargs["student_with_id"]
        args = (no_id, with_id)

    if len(args) == 1:
        entity = args[0]
        assert "id" in entity
        assert isinstance(entity["id"], int)
        assert entity["id"] > 0
        return

    if len(args) == 2:
        no_id, with_id = args
        # ensure all provided keys in no_id are present in with_id with same values
        assert no_id.items() <= with_id.items()
        # with_id may include optional keys (like class_id), so require that it
        # at minimum contains the keys from no_id plus `id`.
        assert set(with_id) >= set(no_id) | {"id"}
        assert isinstance(with_id["id"], int)
        assert with_id["id"] > 0
        return

    raise TypeError("check_identical_except_id accepts 1 or 2 positional arguments")


def sample_student():
    return {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}


def sample_parent():
    return {
        "name": "Stepan",
        "surname": "Bratkovskyi",
        "birthday": "1991-03-04",
        "phone": "+380773147189",
        "email": "stepanbb@gmail.com",
    }


def sample_teacher():
    return {
        "name": "Panas",
        "surname": "Semerchenko",
        "birthday": "1988-08-14",
        "phone": "+380773147189",
        "email": "panassem@gmail.com",
        "subjects": "math, computer science",
        "classes": "2, 3, 4, 5, 8, 9",
    }
