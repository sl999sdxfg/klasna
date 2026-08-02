from sqlmodel import SQLModel, Session
from fastapi import HTTPException


def get_or_404[T: SQLModel](model: type[T], id: int, session: Session) -> T:
    obj: T | None = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"no {model.__name__} with id={id}")
    return obj
