from fastapi import APIRouter
from api.v1.health import router as health
from api.v1.get_seats import router as seats
from api.v1.reserve_seat import router as reserve_seat
from api.v1.confirm_seat import router as confirm_seat

router = APIRouter()

router.include_router(health,prefix="/health",tags=["health check"])
router.include_router(seats,prefix="/get_seats",tags=["get seat list"])
router.include_router(reserve_seat,prefix="/reserve_seat",tags=["reserve seat for user"])
router.include_router(confirm_seat,prefix="/book_seat",tags=["book seat for this user"])