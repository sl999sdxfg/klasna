from typing import TypeVar

from fastapi import HTTPException
from sqlmodel import Session, SQLModel

T = TypeVar("T", bound=SQLModel)


def get_or_404(model: type[T], id: int, session: Session) -> T:
    obj: T | None = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"no {model.__name__} with id={id}")
    return obj
