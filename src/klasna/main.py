from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
from datetime import date
from contextlib import asynccontextmanager


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine("sqlite:///database.db")
    yield
    SQLModel.metadata.create_all(engine)  # type: ignore


app = FastAPI(lifespan=lifespan)
