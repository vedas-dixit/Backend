from pydantic import BaseModel, Field
import uuid
# request schema
class User(BaseModel):
    user_name: str
    password: str

class UserInDB(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str
    password: str
    role: str = "user"