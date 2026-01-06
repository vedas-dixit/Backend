from fastapi import APIRouter
from models.models import ApiRequest
router = APIRouter()

@router.post("/")
def health_check(request: ApiRequest):
    #dummy
    request.user_id
    request.ip_address
    return{
        "status": "sucess"
    }