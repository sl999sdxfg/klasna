from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, select
from .database import engine, get_session
from .models import Student, StudentCreate, StudentUpdate
from .utils import get_or_404


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


@app.patch("/students/{id}")
def update_student(
    id: int, student: StudentUpdate, session: Session = Depends(get_session)
) -> Student:
    db_student: Student = get_or_404(Student, id, session)
    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    session.add(db_student)
    session.commit()
    print(db_student)
    session.refresh(db_student)
    print(db_student)
    return db_student
