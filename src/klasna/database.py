from collections.abc import Generator

from sqlalchemy.engine.base import Engine
from sqlmodel import Session, create_engine

engine: Engine = create_engine("sqlite:///database.db")


def get_session() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session
