import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.staticfiles import (
    StaticFiles
)

from routers.routers import (
    router
)


app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app)
