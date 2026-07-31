from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date
from contextlib import asynccontextmanager

engine = create_engine("sqlite:///database.db")


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date


class StudentCreate(SQLModel):
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


@app.post("/students/")
def create_student(
    student: StudentCreate, session: Session = Depends(get_session)
) -> Student:
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student


def get_or_404[T: SQLModel](model: type[T], id: int, session: Session) -> T:
    obj: T | None = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"no {model.__name__} with id={id}")
    return obj


@app.get("/students/{id}")
def get_student(id: int, session: Session = Depends(get_session)) -> Student:
    student: Student = get_or_404(Student, id, session)
    return student


@app.get("/students/")
def get_all_students(session: Session = Depends(get_session)) -> list[Student]:
    selection = select(Student)
    students: list[Student] = session.exec(selection).all()
    return students


@app.delete("/students/{id}")
def delete_student(id: int, session: Session = Depends(get_session)) -> Student:
    student: Student = get_or_404(Student, id, session)
    session.delete(student)
    session.commit()
    return student
