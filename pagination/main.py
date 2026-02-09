from fastapi import FastAPI
from api.v1.router import router as api_router
app = FastAPI()

app.include_router(api_router,prefix="/api/v1",tags=["api route"])

@app.get("/")
def test_func():
    return {
        "status":"ok"
    }