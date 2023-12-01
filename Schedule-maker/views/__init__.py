__all__ = (
    'templates'
)


from fastapi.templating import (
    Jinja2Templates
)

templates = Jinja2Templates(directory='templates')
