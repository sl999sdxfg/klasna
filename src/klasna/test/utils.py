MISSING_ID = 999_999_999


def student_data(**overrides: str) -> dict[str, str]:
    data: dict[str, str] = {
        "name": "Ivan",
        "surname": "Bratkovskyi",
        "birthday": "2012-01-11",
    }
    data.update(overrides)
    return data


def parent_data(**overrides: str) -> dict[str, str]:
    data: dict[str, str] = {
        "name": "Stepan",
        "surname": "Bratkovskyi",
        "birthday": "1991-03-04",
        "phone": "+380773147189",
        "email": "stepanbb@gmail.com",
    }
    data.update(overrides)
    return data


def teacher_data(**overrides: str) -> dict[str, str]:
    data: dict[str, str] = {
        "name": "Panas",
        "surname": "Semerchenko",
        "birthday": "1988-08-14",
        "phone": "+380773147189",
        "email": "panassem@gmail.com",
        "subjects": "math, computer science",
        "classes": "2, 3, 4, 5, 8, 9",
    }
    data.update(overrides)
    return data
