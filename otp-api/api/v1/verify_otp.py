from fastapi import APIRouter, HTTPException, status
from models.VerifyOtpModel import VerifyOtpModel
from service.verify_opt_service import verify_otp_service
from exceptions.exceptions import UserAlreadyAuthenticated, UserDoesNotExist,OTPExpired,InvalidOTP

router = APIRouter()



@router.post("/")
def verify_otp(request: VerifyOtpModel):
    try:
        verify_otp_service(request.email,request.otp)
        return {
            "message": "User signed in successfully"
        }
    except UserDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user does not exist"
        )
    except OTPExpired:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Expired OTP"
        )
    except InvalidOTP:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="wrong OTP! Try again"
        )
    except UserAlreadyAuthenticated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already authenticated"
        )
