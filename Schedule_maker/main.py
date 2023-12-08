from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from uvicorn import run

from sqlalchemy import select

from starlette.middleware.sessions import SessionMiddleware

from routers.routers import router
from config.settings import settings
from models.db import db
from models import User

app = FastAPI(debug=True)
app.include_router(
    router,
    prefix=''
)


app.mount("/static", settings.static_files, name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    run(app)
