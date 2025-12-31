from fastapi import APIRouter, HTTPException, status
router = APIRouter()
from models.GetOtpModel import GetOtpModel
from service.send_otp_service import send_otp_service as send_otp
from exceptions.exceptions import OTPRecentlySent, MaxOTPRequestsReached

@router.post("/")
async def get_otp(request: GetOtpModel):
    try:
        send_otp(request.email)
        return {"message": "OTP sent successfully."}
    
    except OTPRecentlySent:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OTP already sent recently. Please wait before requesting again."
        )
    
    except MaxOTPRequestsReached:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Maximum OTP requests reached. Please try again later."
        )

