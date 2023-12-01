from fastapi_utils.inferring_router import (
    InferringRouter
)
from fastapi import (
    APIRouter
)
from fastapi_users import (
    FastAPIUsers
)

from uuid import (
    UUID
)

from views.index import router as index_router
from views.auth import router as auth_router

from secure import (
    auth_backend
)
from models import (
    User
)
from cruds import (
    get_user_manager
)
from models import (
    UserRead,
    UserCreate
)


router = InferringRouter()

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend]
)

router.include_router(
    index_router,
    prefix=''
)

router.include_router(
    auth_router,
    prefix=''
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)
