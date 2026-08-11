import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .. import database
from ..database import get_session
from ..main import app


class Endpoints:
    BASE_URL = "http://127.0.0.1:8000"
    STUDENTS = f"{BASE_URL}/students/"
    PARENTS = f"{BASE_URL}/parents/"
    TEACHERS = f"{BASE_URL}/teachers/"


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(autouse=True)
def _bind_client(client):
    # Inject common names into the test module namespace so tests can
    # refer to `client`, `baseurl`, and endpoint names directly.
    request = pytest.request if hasattr(pytest, "request") else None
    # Prefer using the pytest `request` fixture when available; fall back
    # to setting in this module's globals for compatibility.
    try:
        # pytest will supply a `request` fixture to this function if requested
        # but since we didn't declare it, use the module of the currently
        # running test via inspect
        import inspect

        frame = inspect.currentframe()
        # walk up to find the test frame
        while frame:
            if (
                frame.f_code.co_name.startswith("pytest_")
                or "pytest" in frame.f_globals
            ):
                break
            frame = frame.f_back
    except Exception:
        frame = None

    # Best-effort: set attributes on the test module where possible
    try:
        # Use pytest's request if available from the fixture system

        # If pytest has a currently active request, use it to get module
        # (this works when pytest hands a request to fixtures). Otherwise,
        # set names in this module so tests that import these names still
        # find them.

        # Try to find the calling test module via the call stack
        test_module = None
        for fr in inspect.stack():
            mod = inspect.getmodule(fr.frame)
            if mod and mod.__name__.startswith("test"):
                test_module = mod
                break
        if test_module is not None:
            test_module.client = client
            test_module.baseurl = Endpoints.BASE_URL
            test_module.parent_endpoint = Endpoints.PARENTS
            test_module.teacher_endpoint = Endpoints.TEACHERS
            # provide HTTP status constants
            from fastapi import status as _status

            test_module.status = _status
        else:
            globals()["client"] = client
            globals()["baseurl"] = Endpoints.BASE_URL
            globals()["parent_endpoint"] = Endpoints.PARENTS
            globals()["teacher_endpoint"] = Endpoints.TEACHERS
            from fastapi import status as _status

            globals()["status"] = _status
    except Exception:
        # fallback: set in this module's globals
        globals()["client"] = client
        globals()["baseurl"] = Endpoints.BASE_URL
        globals()["parent_endpoint"] = Endpoints.PARENTS
        globals()["teacher_endpoint"] = Endpoints.TEACHERS
        from fastapi import status as _status

        globals()["status"] = _status


@pytest.fixture(autouse=True)
def db_setup():
    database.engine = test_engine
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


def get_test_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def created_student(client):
    student_data = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    post_result = client.post(Endpoints.STUDENTS, json=student_data)
    return post_result.json()


@pytest.fixture
def created_parent(client):
    parent_data = {
        "name": "Stepan",
        "surname": "Bratkovskyi",
        "birthday": "1991-03-04",
        "phone": "+380975840179",
        "email": "stepanbb@gmail.com",
        "students": [],
    }
    post_result = client.post(Endpoints.PARENTS, json=parent_data)
    return post_result.json()


@pytest.fixture
def created_teacher(client):
    teacher_data = {
        "name": "Panas",
        "surname": "Semerchenko",
        "birthday": "1988-08-14",
        "phone": "+380773147189",
        "email": "panassem@gmail.com",
        "subjects": "math, computer science",
        "classes": "2, 3, 4, 5, 8, 9",
    }
    post_result = client.post(Endpoints.TEACHERS, json=teacher_data)
    return post_result.json()
