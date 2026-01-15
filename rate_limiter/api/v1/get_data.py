from fastapi import APIRouter
from models.models import ApiRequest
from services.check_rate_limit import check_rate_limit
router = APIRouter()

@router.post("/")
def get_data(request: ApiRequest):
    #dummy
    request.user_id
    request.ip_address
    try:
        check_rate_limit(request.user_id,request.ip_address)
        return{
        "status": "sucess"
        }
    except Exception as e:
        return{
            "status": "failed",
            "reason": str(e)
        }