from fastapi_utils.inferring_router import InferringRouter


from Schedule_maker.views.auth import router as auth_router
from Schedule_maker.views.index import router as index_router
from Schedule_maker.views.tables import router as table_router
from Schedule_maker.views.static_pages import router as static_pages_router
from Schedule_maker.views.schedule import router as schedule_router


router = InferringRouter()


router.include_router(
    auth_router,
    prefix=''
)

router.include_router(
    index_router,
    prefix=''
)

router.include_router(
    table_router,
    prefix='/tables'
)

router.include_router(
    static_pages_router,
    prefix='/static-pages'
)

router.include_router(
    schedule_router,
    prefix='/schedule'
)
