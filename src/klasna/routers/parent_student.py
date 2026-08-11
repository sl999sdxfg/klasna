from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Parent, Student, StudentParentLink, StudentWithParents
from ..utils import get_or_404

router = APIRouter()


@router.post("/students/{student_id}/parents/{parent_id}/")
def link_student_parent(
    student_id: int, parent_id: int, session: Session = Depends(get_session)
) -> StudentWithParents:
    db_student = get_or_404(Student, student_id, session)
    db_parent = get_or_404(Parent, parent_id, session)
    # Prevent duplicate links
    if db_parent in db_student.parents:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="already linked"
        )
    student_parent_link = StudentParentLink(student_id=student_id, parent_id=parent_id)
    session.add(student_parent_link)
    session.commit()
    return get_or_404(Student, student_id, session)


@router.delete("/students/{student_id}/parents/{parent_id}/")
def unlink_student_parent(
    student_id: int, parent_id: int, session: Session = Depends(get_session)
) -> StudentWithParents:
    db_student = get_or_404(Student, student_id, session)
    # to ensure parent exists but should work anyway if no bugs
    db_parent = get_or_404(Parent, parent_id, session)
    if db_parent not in db_student.parents:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="object do not relate"
        )

    statement = select(StudentParentLink).where(
        StudentParentLink.student_id == student_id,
        StudentParentLink.parent_id == parent_id,
    )
    link = session.exec(statement).first()
    if link is None:
        raise HTTPException(status_code=404, detail="link not found")
    session.delete(link)
    session.commit()
    return get_or_404(Student, student_id, session)
