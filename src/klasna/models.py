from datetime import date
from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date


class StudentCreate(SQLModel):
    name: str
    surname: str
    birthday: date


class StudentUpdate(SQLModel):
    name: str | None = None
    surname: str | None = None
    birthday: date | None = None


class Parent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date
    phone: str
    email: str


class ParentCreate(SQLModel):
    name: str
    surname: str
    birthday: date
    phone: str
    email: str


class ParentUpdate(SQLModel):
    name: str | None = None
    surname: str | None = None
    birthday: date | None = None
    phone: str | None = None
    email: str | None = None
