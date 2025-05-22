from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def test_trade():
    return {"message": "trade router is working"}
