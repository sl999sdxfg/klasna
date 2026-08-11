from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import get_session
from ..models import Teacher, TeacherCreate
from ..utils import get_or_404

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/{id}")
def get_teacher(id: int, session: Session = Depends(get_session)) -> Teacher:
    teacher: Teacher = get_or_404(Teacher, id, session)
    return teacher


@router.post("/")
def create_teacher(
    teacher: TeacherCreate, session: Session = Depends(get_session)
) -> Teacher:
    db_teacher = Teacher.model_validate(teacher)
    session.add(db_teacher)
    session.commit()
    session.refresh(db_teacher)
    return db_teacher


@router.get("/")
def get_all_teachers(session: Session = Depends(get_session)) -> list[Teacher]:
    selection = select(Teacher)
    teachers: list[Teacher] = session.exec(selection).all()
    return teachers


@router.delete("/{id}")
def delete_teacher(id: int, session: Session = Depends(get_session)) -> Teacher:
    teacher: Teacher = get_or_404(Teacher, id, session)
    session.delete(teacher)
    session.commit()
    return teacher
