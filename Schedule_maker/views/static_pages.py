from fastapi import APIRouter, Request

from Schedule_maker.config import settings
from Schedule_maker.cruds.UserManager import user_manager

router = APIRouter()


class SplashScreenView:
    @staticmethod
    @router.get('/')
    async def index(request: Request):
        return settings.templates.TemplateResponse('index.html', {
            'request': request,
        })


class AboutView:
    @staticmethod
    @router.get('/about-authors')
    async def about_authors(request: Request):
        return settings.templates.TemplateResponse('about_authors.html', {
            'title': 'About Authors',
            'request': request,
            'user': await user_manager.get_user_or_none(request.cookies)
        })

    @staticmethod
    @router.get('/about-site')
    async def about_site(request: Request):
        return settings.templates.TemplateResponse('about_site.html', {
            'title': 'About Site',
            'request': request,
            'user': await user_manager.get_user_or_none(request.cookies)
        })
