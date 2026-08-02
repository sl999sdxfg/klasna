from datetime import date
from sqlmodel import Field, Relationship, SQLModel


class StudentParentLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parent_id: int = Field(foreign_key="parent.id")
    student_id: int = Field(foreign_key="student.id")


class StudentParentLinkCreate(SQLModel):
    parent_id: int
    student_id: int


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date
    parents: list["Parent"] = Relationship(
        back_populates="students", link_model=StudentParentLink
    )


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
    students: list["Student"] = Relationship(
        back_populates="parents", link_model=StudentParentLink
    )


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
