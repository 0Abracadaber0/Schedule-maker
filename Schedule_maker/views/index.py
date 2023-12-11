from fastapi import APIRouter, Request

from Schedule_maker.config import settings
from Schedule_maker.cruds.UserManager import user_manager

router = APIRouter()


class IndexView:
    @staticmethod
    @router.get('/main')
    async def index(
            request: Request,
    ):
        return settings.templates.TemplateResponse('main.html', {
            'title': 'Schedule Maker',
            'request': request,
            'user': await user_manager.get_user_or_none(request.cookies)
        })


class SplashScreenView:
    @staticmethod
    @router.get('/')
    async def index(
            request: Request,
    ):
        return settings.templates.TemplateResponse('index.html', {
            'request': request,
        })
