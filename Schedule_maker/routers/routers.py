from fastapi_utils.inferring_router import InferringRouter


from Schedule_maker.views.auth import router as auth_router
from Schedule_maker.views.index import router as index_router
from Schedule_maker.views.tables import router as table_router


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
