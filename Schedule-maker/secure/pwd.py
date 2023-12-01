from dotenv import (
    load_dotenv
)
from passlib.context import (
    CryptContext
)
from fastapi_users.authentication import (
    BearerTransport,
    JWTStrategy,
    AuthenticationBackend
)
from fastapi_users.password import (
    PasswordHelper
)
from os import (
    getenv
)

load_dotenv()

SECRET = getenv('SECRET')

pwd_context = CryptContext(schemes=["sha256_crypt", "des_crypt"])
bearer_transport = BearerTransport(tokenUrl='/auth/jwt/login')
password_helper = PasswordHelper(pwd_context)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)
