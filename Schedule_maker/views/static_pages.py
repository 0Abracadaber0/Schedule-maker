from fastapi import APIRouter, Request

from Schedule_maker.config import settings

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
            'request': request
        })

    @staticmethod
    @router.get('/about-site')
    async def about_site(request: Request):
        return settings.templates.TemplateResponse('about_site.html', {
            'request': request
        })
