from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine
from datetime import date
from contextlib import asynccontextmanager

engine = create_engine("sqlite:///database.db")


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    surname: str
    birthday: date


class StudentCreate(SQLModel):
    name: str
    surname: str
    birthday: date


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # type: ignore
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/students/")
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    student = Student.model_validate(student)
    session.add(student)
    session.commit()
    session.refresh(student)
    print(student)
    return student
