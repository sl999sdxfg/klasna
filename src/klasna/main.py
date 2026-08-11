from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from . import database
from .routers.parent_student import router as parent_student_router
from .routers.parents import router as parent_router
from .routers.students import router as student_router
from .routers.teacher import router as teacher_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(database.engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(student_router)
app.include_router(parent_router)
app.include_router(parent_student_router)
app.include_router(teacher_router)
