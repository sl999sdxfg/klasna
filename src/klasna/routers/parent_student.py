from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..database import get_session
from ..models import Parent, Student, StudentWithParents
from ..utils import get_or_404, save

router = APIRouter()


@router.post("/students/{student_id}/parents/{parent_id}/")
def link_student_parent(
    student_id: int, parent_id: int, session: Session = Depends(get_session)
) -> StudentWithParents:
    student = get_or_404(Student, student_id, session)
    parent = get_or_404(Parent, parent_id, session)
    if parent in student.parents:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="already linked"
        )
    student.parents.append(parent)
    return save(session, student)


@router.delete("/students/{student_id}/parents/{parent_id}/")
def unlink_student_parent(
    student_id: int, parent_id: int, session: Session = Depends(get_session)
) -> StudentWithParents:
    student = get_or_404(Student, student_id, session)
    parent = get_or_404(Parent, parent_id, session)
    if parent not in student.parents:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="object do not relate"
        )
    student.parents.remove(parent)
    return save(session, student)
