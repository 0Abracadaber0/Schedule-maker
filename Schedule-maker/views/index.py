from fastapi import (
    APIRouter,
    Request
)
from fastapi.templating import (
    Jinja2Templates
)

from views import (
    templates
)

router = APIRouter()


class IndexView:
    @staticmethod
    @router.get('/')
    async def index(request: Request):
        return templates.TemplateResponse('index.html', {
            'request': request,
        })
