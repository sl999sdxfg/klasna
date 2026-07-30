from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine
from typing import Optional
from datetime import date
from contextlib import asynccontextmanager

engine = create_engine("sqlite:///database.db")


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # type: ignore
    yield


app = FastAPI(lifespan=lifespan)
