from fastapi import FastAPI, APIRouter
from api.v1 import auth

app = FastAPI()
app.include_router(auth.router, prefix="/auth")


@app.get("/")
def health():
    return {"status":"healthy"}
