from fastapi import APIRouter
from api.v1.process_request import router as processreqrouter
router = APIRouter()

router.include_router(processreqrouter,prefix="/process-request",tags=["process user request"])