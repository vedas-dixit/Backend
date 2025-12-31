from pydantic import BaseModel

class GetOtpModel(BaseModel):
    email: str