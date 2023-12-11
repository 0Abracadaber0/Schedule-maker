import jwt

from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select
from starlette import status

from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.security.pwd import oauth2_scheme
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager
from Schedule_maker.models.db import Database, db
from Schedule_maker.models.core import User


class UserManager:
    def __init__(self, _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings
                 ):
        self.db = db
        self.password_manager = password_manager
        self.settings = _settings

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

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return False
        if not self.password_manager.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
        user: User = await self.get_user_by_email(email=payload.get('email'))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def get_current_verified_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
        user: User = await self.get_user_by_email(email=payload.get('email'))
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

    async def get_user_or_none(self, cookies):
        data = cookies.get('access_token')
        if data:
            token = data.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            return await self.get_user_by_id(payload['id'])
        return None


user_manager = UserManager(
    _db=db,
    _password_manager=password_manager,
    _settings=settings
)
