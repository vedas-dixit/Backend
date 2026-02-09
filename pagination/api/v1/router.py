from fastapi import APIRouter
from api.v1 import getdata
router = APIRouter()

router.include_router(getdata.router,prefix="/items",tags=["get paginated items"])
