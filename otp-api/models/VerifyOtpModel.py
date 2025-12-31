from pydantic import BaseModel, Field

class VerifyOtpModel(BaseModel):
    email: str
    otp: str