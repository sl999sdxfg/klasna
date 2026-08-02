from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..models import Student, StudentCreate, StudentUpdate
from ..utils import get_or_404

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/{id}")
def get_student(id: int, session: Session = Depends(get_session)) -> Student:
    student: Student = get_or_404(Student, id, session)
    return student


@router.post("/")
def create_student(
    student: StudentCreate, session: Session = Depends(get_session)
) -> Student:
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student


@router.get("/")
def get_all_students(session: Session = Depends(get_session)) -> list[Student]:
    selection = select(Student)
    students: list[Student] = session.exec(selection).all()
    return students


@router.delete("/{id}")
def delete_student(id: int, session: Session = Depends(get_session)) -> Student:
    student: Student = get_or_404(Student, id, session)
    session.delete(student)
    session.commit()
    return student


@router.patch("/{id}")
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
