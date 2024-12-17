import jwt
from datetime import timedelta, datetime
from passlib.context import CryptContext

from starlette.config import Config

from authlib.integrations.starlette_client import OAuth

from Schedule_maker.config import settings
from .cookie import OAuth2PasswordBearerWithCookie

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearerWithCookie(token_url='login')

config_data = {'GOOGLE_CLIENT_ID': settings.CLIENT_ID, 'GOOGLE_CLIENT_SECRET': settings.CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'https://classify.by/google-login'
    }
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

