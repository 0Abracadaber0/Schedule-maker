import jwt

from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from starlette import status

from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.security.pwd import oauth2_scheme
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager
from .db import Database, db
from .core import User


class UserManager:
    def __init__(self, _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings
                 ):
        self.db = db
        self.password_manager = password_manager
        self.settings = _settings

    async def get_user_by_username(self, username: str) -> User | None:
        async with self.db.engine.connect() as session:
            coroutine_user = await session.execute(select(User).where(User.username == username))
        user = coroutine_user.first()
        if not user:
            return None
        return user

    async def update_user(
            self, _id: UUID, username: str = None,
            password: str = None, email: str = None
    ) -> None:
        try:
            user = await self.get_user_by_username(username)
            if not user:
                raise Exception('User doesnt exist')
            if username is not None:
                user.username = username
            if username is None:
                username = user.username
            if password is not None:
                user.hashed_password = self.password_manager.get_password_hash(password)
            if password is None:
                password = user.hashed_password
            if email is not None:
                user.email = email
            if email is None:
                email = user.email
            async with self.db.engine.connect() as session:
                session.execute(update(User).where(User.id == _id).values(
                    username=username,
                    hashed_password=password,
                    email=email
                ))
                await session.commit()
        except Exception as err:
            print(err)

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.db.engine.connect() as session:
            coroutine_user = await session.execute(select(User).where(User.email == email))
        user = coroutine_user.first()
        if not user:
            return None
        return user

    async def get_user_by_id(self, _id: str):
        async with self.db.engine.connect() as session:
            coroutine_user = await session.execute(select(User).where(User.id == _id))
        user = coroutine_user.first()
        if not user:
            return None
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user_by_username(username)
        if not user:
            return False
        if not self.password_manager.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
        user: User = await self.get_user_by_username(username=payload.get('username'))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def get_current_verified_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
        user: User = await self.get_user_by_username(username=payload.get('username'))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User isn't verified",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user


user_manager = UserManager(
    _db=db,
    _password_manager=password_manager,
    _settings=settings
)
