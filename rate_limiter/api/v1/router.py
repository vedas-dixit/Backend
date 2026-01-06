from fastapi import APIRouter
from api.v1.health import router as health_check
from api.v1.get_data import router as get_data

router = APIRouter()
router.include_router(health_check,prefix="/health",tags=["health check api"])
router.include_router(get_data,prefix="/get_data",tags=["fetching data"])
