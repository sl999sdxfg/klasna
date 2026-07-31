from fastapi.testclient import TestClient
from main import app, get_session
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


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)
SQLModel.metadata.create_all(test_engine)
