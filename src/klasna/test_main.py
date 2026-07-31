from fastapi.testclient import TestClient
from .main import app, get_session
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_test_session():
    with Session(test_engine) as session:
        yield session


SQLModel.metadata.create_all(test_engine)

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

baseurl = "http://127.0.0.1"
student_endpoint = baseurl + "/students/"


def test_student_creation():
    student_ivan = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    post_result: dict = client.post(
        student_endpoint,
        json=student_ivan,
    ).json()

    assert student_ivan.items() <= post_result.items()
    assert post_result["id"] is not None
    assert isinstance(post_result["id"], int)
    assert post_result["id"] >= 0


def test_student_get():
    student_ivan = {"name": "Ivan", "surname": "Bratkovskyi", "birthday": "2012-01-11"}
    post_result: dict = client.post(
        student_endpoint,
        json=student_ivan,
    ).json()
    print(post_result)
    get_result: dict = client.get(f"{student_endpoint}{post_result["id"]}").json()
    assert get_result.items() == post_result.items()
    assert get_result["id"] is not None
    assert isinstance(post_result["id"], int)
    assert get_result["id"] >= 0


def test_student_delete():
    return


def test_student_update():
    return


def test_all_students_get():
    return
