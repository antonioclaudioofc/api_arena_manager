from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import StatementError

from app.core.database import engine, Base
from app.core.exception_handlers import http_exception_handler, sql_exception_handler, validation_exception_handler
from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router
from app.modules.arena.router import router as arena_router
from app.modules.court.router import router as court_router
from app.modules.schedule.router import router as schedule_router
from app.modules.reservation.router import router as reservation_router
from app.modules.catalog.router import router as catalog_router


app = FastAPI(title="Arena Manager")

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    StatementError,
    sql_exception_handler
)

origins = ["*"]

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to the Arena Manager API"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(arena_router)
app.include_router(court_router)
app.include_router(schedule_router)
app.include_router(reservation_router)
app.include_router(catalog_router)
