from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import Parent, ParentCreate, ParentWithStudents
from ..utils import create, delete, get_or_404, list_all

router = APIRouter(prefix="/parents", tags=["parents"])


@router.get("/{id}")
def get_parent(id: int, session: Session = Depends(get_session)) -> ParentWithStudents:
    return get_or_404(Parent, id, session)


@router.post("/")
def create_parent(
    parent: ParentCreate, session: Session = Depends(get_session)
) -> Parent:
    return create(session, Parent, parent)


@router.get("/")
def get_all_parents(session: Session = Depends(get_session)) -> list[Parent]:
    return list_all(session, Parent)


@router.delete("/{id}")
def delete_parent(id: int, session: Session = Depends(get_session)) -> Parent:
    return delete(session, get_or_404(Parent, id, session))
