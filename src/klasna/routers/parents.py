from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..models import Parent, ParentCreate, ParentWithStudents
from ..utils import get_or_404

router = APIRouter(prefix="/parents", tags=["parents"])


@router.get("/{id}")
def get_parent(id: int, session: Session = Depends(get_session)) -> ParentWithStudents:
    parent: Parent = get_or_404(Parent, id, session)
    return parent


@router.post("/")
def create_parent(
    parent: ParentCreate, session: Session = Depends(get_session)
) -> Parent:
    db_parent = Parent.model_validate(parent)
    session.add(db_parent)
    session.commit()
    session.refresh(db_parent)
    return db_parent


@router.get("/")
def get_all_parents(session: Session = Depends(get_session)) -> list[Parent]:
    selection = select(Parent)
    parents: list[Parent] = session.exec(selection).all()
    return parents


@router.delete("/{id}")
def delete_parent(id: int, session: Session = Depends(get_session)) -> Parent:
    parent: Parent = get_or_404(Parent, id, session)
    session.delete(parent)
    session.commit()
    return parent
