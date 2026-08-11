from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class Class(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    grade: int
    section: str
    school_year_id: int
    homeroom_teacher_id: int | None = None

    students: list["Student"] = Relationship(back_populates="class_")


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

    class_id: int | None = Field(default=None, foreign_key="class.id")
    class_: Class | None = Relationship(back_populates="students")


class StudentCreate(SQLModel):
    name: str
    surname: str
    birthday: date


class StudentUpdate(SQLModel):
    name: str | None = None
    surname: str | None = None
    birthday: date | None = None


class StudentWithParents(SQLModel):
    id: int
    name: str
    surname: str
    birthday: date
    parents: list["Parent"] = Field(default_factory=list)


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


class ParentWithStudents(SQLModel):
    id: int
    name: str
    surname: str
    birthday: date
    phone: str
    email: str
    students: list[Student] = Field(default_factory=list)


class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date
    phone: str | None = None
    email: str | None = None
    subjects: str
    classes: str
    # list["Subject"] = Relationship(
    #     back_populates="subject", link_model=TeacherSubjectLink
    # )


class TeacherCreate(SQLModel):
    name: str
    surname: str
    birthday: date
    phone: str | None = None
    email: str | None = None
    subjects: str
    classes: str


class ClassCreate(SQLModel):
    grade: int
    section: str
    school_year_id: int
    homeroom_teacher_id: int | None = None


class ClassWithStudents(SQLModel):
    grade: int
    section: str
    school_year_id: int
    homeroom_teacher_id: int | None = None
