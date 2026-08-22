from datetime import date
from enum import StrEnum, auto

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel


class Subject(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Class(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
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


class PersonBase(SQLModel):
    name: str
    surname: str
    birthday: date


class PersonUpdate(SQLModel):
    name: str | None = None
    surname: str | None = None
    birthday: date | None = None


class Student(PersonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parents: list["Parent"] = Relationship(
        back_populates="students", link_model=StudentParentLink
    )

    class_id: int | None = Field(default=None, foreign_key="class.id")
    class_: Class | None = Relationship(back_populates="students")


class StudentCreate(PersonBase):
    pass


class StudentUpdate(PersonUpdate):
    pass


class StudentWithParents(PersonBase):
    id: int
    parents: list["Parent"] = Field(default_factory=list)


class ParentBase(PersonBase):
    phone: str
    email: str


class Parent(ParentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    students: list["Student"] = Relationship(
        back_populates="parents", link_model=StudentParentLink
    )


class ParentCreate(ParentBase):
    pass


class ParentUpdate(PersonUpdate):
    phone: str | None = None
    email: str | None = None


class ParentWithStudents(ParentBase):
    id: int
    students: list[Student] = Field(default_factory=list)


class TeacherBase(PersonBase):
    phone: str | None = None
    email: str | None = None
    subjects: str
    classes: str


class Teacher(TeacherBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TeacherCreate(TeacherBase):
    pass


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


class Lesson(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    class_id: int = Field(foreign_key="class.id")
    teacher_id: int = Field(foreign_key="teacher.id")
    date: date


class AttendanceStatus(StrEnum):
    ABSENT = auto()
    SICK = auto()
    VALID_REASON = auto()


class Grade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    lesson_id: int = Field(foreign_key="lesson.id")
    score: int | None = None
    status: AttendanceStatus | None = None

    @model_validator(mode="after")
    def grade_validate(self) -> "Grade":
        if self.score is not None and (self.score < 1 or self.score > 12):
            raise ValueError("Grade should be in range 1-12")
        return self

    @model_validator(mode="after")
    def grade_and_status_not_both_set(self) -> "Grade":
        if self.score is not None and self.status is not None:
            raise ValueError(
                "Grade and attendance status can not be set simultaneously"
            )
        return self


class GradeCreate(SQLModel):
    student_id: int
    lesson_id: int
    score: int | None = None
    status: AttendanceStatus | None = None


class LessonCreate(SQLModel):
    subject_id: int
    class_id: int
    teacher_id: int
    date: date
