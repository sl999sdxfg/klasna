from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import Student, StudentCreate, StudentUpdate, StudentWithParents
from ..utils import apply_update, create, delete, get_or_404, list_all, to_schema

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/{id}")
def get_student(id: int, session: Session = Depends(get_session)) -> StudentWithParents:
    return to_schema(StudentWithParents, get_or_404(Student, id, session))


@router.post("/")
def create_student(
    student: StudentCreate, session: Session = Depends(get_session)
) -> Student:
    return create(session, Student, student)


@router.get("/")
def get_all_students(session: Session = Depends(get_session)) -> list[Student]:
    return list_all(session, Student)


@router.delete("/{id}")
def delete_student(id: int, session: Session = Depends(get_session)) -> Student:
    return delete(session, get_or_404(Student, id, session))


@router.patch("/{id}")
def update_student(
    id: int, student: StudentUpdate, session: Session = Depends(get_session)
) -> Student:
    return apply_update(session, get_or_404(Student, id, session), student)
