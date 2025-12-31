from fastapi import APIRouter
from api.v1.get_otp import router as verify_otp
from api.v1.verify_otp import router as verify_otp_router

router = APIRouter()
router.include_router(verify_otp,prefix="/get-otp", tags=["Get OTP"])
router.include_router(verify_otp_router,prefix="/verify-otp", tags=["Verify OTP"])