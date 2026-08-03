from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..models import Student, Parent, StudentParentLink, StudentWithParents
from ..utils import get_or_404

router = APIRouter()


@router.post("/students/{student_id}/parents/{parent_id}/")
def link_student_parent(
    student_id: int, parent_id: int, session: Session = Depends(get_session)
) -> StudentWithParents:
    db_student = get_or_404(Student, student_id, session)
    db_parent = get_or_404(Parent, parent_id, session)
    student_parent_link = StudentParentLink(student_id=student_id, parent_id=parent_id)
    session.add(student_parent_link)
    session.commit()
    return get_or_404(Student, student_id, session)
