from fastapi import (
    APIRouter,
    Request,
    Depends,
    Form
)
from sqlalchemy import select
from sqlalchemy.orm import (
    Session
)
from starlette.exceptions import (
    HTTPException
)

from views import (
    templates
)
from models import (
    User,
    get_db
)
from secure import (
    pwd_context
)
from cruds import (
    get_user_manager
)
from models import (
    db_get_by_username,
)

router = APIRouter()


class RegistrationView:
    @staticmethod
    @router.get('/registration')
    async def register(request: Request):
        return templates.TemplateResponse('registration.html', {
            'request': request,
        })

    @staticmethod
    @router.post('/registration')
    async def register(request: Request, email: str = Form(),
                       username: str = Form(), password: str = Form(),
                       db: Session = Depends(get_db)
                       ):
        async with db as session:
            coroutine_user = await session.execute(select(User).where(User.username == username))
        user = coroutine_user.scalar()
        if not user:
            print('finally')
            user = User(
                username=username,
                email=email,
                hashed_password=pwd_context.hash(password)
            )
            async with db as session:
                session.add(user)
                await session.commit()
            return {'registration': 'success'}
        else:
            raise HTTPException(
                status_code=400,
                detail='User already exists'
            )
