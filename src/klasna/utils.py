from fastapi import HTTPException
from sqlmodel import Session, SQLModel, select


def get_or_404[T: SQLModel](model: type[T], id: int, session: Session) -> T:
    obj: T | None = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"no {model.__name__} with id={id}")
    return obj


def save[T: SQLModel](session: Session, obj: T) -> T:
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def create[T: SQLModel](session: Session, model: type[T], data: SQLModel) -> T:
    return save(session, model.model_validate(data))


def list_all[T: SQLModel](session: Session, model: type[T]) -> list[T]:
    return list(session.exec(select(model)).all())


def delete[T: SQLModel](session: Session, obj: T) -> T:
    session.delete(obj)
    session.commit()
    return obj


def apply_update[T: SQLModel](session: Session, obj: T, data: SQLModel) -> T:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    return save(session, obj)
