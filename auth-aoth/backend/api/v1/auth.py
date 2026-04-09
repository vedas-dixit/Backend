from fastapi import FastAPI, APIRouter
from services.auth_service import handelLogin,HandelSignup
from models.user import User
router = APIRouter()

@router.post("/login")
def login(user:User):
    return handelLogin(user=user)
    

@router.post("/signup")
def signup(user:User):
    return HandelSignup(user=user)