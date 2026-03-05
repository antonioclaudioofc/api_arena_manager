from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import StatementError

from app.core.database import engine, Base
from app.core.exception_handlers import http_exception_handler, sql_exception_handler, validation_exception_handler

from app.models.arena import Arena
from app.models.court import Court
from app.models.match import Match
from app.models.match_participant import MatchParticipant
from app.models.payment import Payment
from app.models.reservation import Reservation
from app.models.schedule import Schedule
from app.models.user import User

from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router


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
