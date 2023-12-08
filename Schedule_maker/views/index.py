from fastapi import APIRouter, Request, Depends
from typing import Annotated

from Schedule_maker.config import settings

from Schedule_maker.views.auth import verify_token

router = APIRouter()


class IndexView:
    @staticmethod
    @router.get('/')
    async def index(
            request: Request,
    ):
        return settings.templates.TemplateResponse('main.html', {
            'request': request,
            'user': None
        })
