import jwt
import requests

import uuid

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse

from sqlalchemy import update
from sqlalchemy.orm import Session

from starlette import status

from Schedule_maker.models import User
from Schedule_maker.cruds.UserManager import user_manager
from Schedule_maker.security.pwd import create_access_token
from Schedule_maker.security.PasswordManager import password_manager
from Schedule_maker.config import settings
from Schedule_maker.models.db import db
from Schedule_maker.cruds.EmailHandler import email_handler


router = APIRouter()


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user = await user_manager.get_user_by_id(payload.get('id'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_google_user_info(code: str, redirect_uri: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {access_token}"})
    return user_info


class LoginView:
    @staticmethod
    @router.get('/login')
    async def login(request: Request):
        return settings.templates.TemplateResponse(
            'login.html', {
                'request': request,
                "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.CLIENT_ID}"
                       f"&redirect_uri=http://127.0.0.1:8000/google-login&scope=openid%20profile%20email&"
                       f"access_type=offline"
            }
        )

    @staticmethod
    @router.post("/login")
    async def login_for_access_token(
        email: str = Form(), password: str = Form()
    ):
        user = await user_manager.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={
                'id': user.id,
                'email': user.email,
            },
            expires_delta=access_token_expires
        )
        response = RedirectResponse('/main')
        response.set_cookie("access_token", f"Bearer {access_token}", httponly=True)
        response.status_code = 302
        return response


class RegistrationView:
    @staticmethod
    @router.get('/register')
    async def register(request: Request):
        return settings.templates.TemplateResponse(
            'registration.html', {
                'request': request,
                "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.CLIENT_ID}"
                       f"&redirect_uri=http://127.0.0.1:8000/google-register&scope=openid%20profile%20email&"
                       f"access_type=offline"
            }
        )

    @staticmethod
    @router.post('/register')
    async def register(
            email: str = Form(), password: str = Form(),
            db_: Session = Depends(db.get_db)
    ):
        user = await user_manager.get_user_by_email(email)
        if not user:
            user = User(
                email=email,
                hashed_password=password_manager.get_password_hash(password)
            )
            db_.add(user)
            await db_.commit()
            await email_handler.send_verification_email(email, user)
            response = RedirectResponse('/main')
            response.status_code = 302
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail='User already exists'
            )


class LogoutView:
    @staticmethod
    @router.get('/logout')
    async def logout():
        response = RedirectResponse('/main')
        response.delete_cookie('access_token')
        response.status_code = 302
        return response


class GoogleAuthenticationView:
    @staticmethod
    @router.get('/google-login')
    async def google_login(code: str):
        user_info = await get_google_user_info(code, 'http://127.0.0.1:8000/google-login')
        user_json = user_info.json()
        user = await user_manager.get_user_by_email(user_json['email'])
        if user:
            access_token_expires = timedelta(minutes=60)
            access_token = create_access_token(
                data={
                    'id': user.id,
                    'email': user.email,
                },
                expires_delta=access_token_expires
            )
            response = RedirectResponse('/main')
            response.set_cookie("access_token", f"Bearer {access_token}", httponly=True)
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    @router.get('/google-register')
    async def google_register(code: str, db_: Session = Depends(db.get_db)):
        user_info = await get_google_user_info(code, 'http://127.0.0.1:8000/google-register')
        user_json = user_info.json()
        user_exists = await user_manager.get_user_by_id(user_json['id'])
        if not user_exists:
            user = User(
                email=user_json['email'],
                hashed_password=''
            )
            user.is_google_user = True
            user.is_verified = True
            user.id = str(uuid.uuid4())
            db_.add(user)
            await db_.commit()
            access_token_expires = timedelta(minutes=60)
            access_token = create_access_token(
                data={
                    'id': user.id,
                    'email': user.email,
                },
                expires_delta=access_token_expires
            )
            response = RedirectResponse('/main')
            response.set_cookie("access_token", f"Bearer {access_token}", httponly=True)
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=400,
            detail='User already exists'
        )


class EmailVerificationView:
    @staticmethod
    @router.get('/verification')
    async def email_verification(token: str, db_: Session = Depends(db.get_db)):
        user = await verify_token(token)
        if user and not user.is_verified:
            await db_.execute(update(User).where(User.id == user.id).values(is_verified=True))
            await db_.commit()
            response = RedirectResponse('/main')
            access_token_expires = timedelta(minutes=60)
            access_token = create_access_token(
                data={
                    'id': user.id,
                    'email': user.email,
                },
                expires_delta=access_token_expires
            )
            response.delete_cookie('Pycharm-c9023144')
            response.set_cookie('access_token', f'Bearer {access_token}', httponly=True)
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
