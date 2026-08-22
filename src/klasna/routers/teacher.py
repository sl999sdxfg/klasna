from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import Teacher, TeacherCreate
from ..utils import create, delete, get_or_404, list_all

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/{id}")
def get_teacher(id: int, session: Session = Depends(get_session)) -> Teacher:
    return get_or_404(Teacher, id, session)


@router.post("/")
def create_teacher(
    teacher: TeacherCreate, session: Session = Depends(get_session)
) -> Teacher:
    return create(session, Teacher, teacher)


@router.get("/")
def get_all_teachers(session: Session = Depends(get_session)) -> list[Teacher]:
    return list_all(session, Teacher)


@router.delete("/{id}")
def delete_teacher(id: int, session: Session = Depends(get_session)) -> Teacher:
    return delete(session, get_or_404(Teacher, id, session))
