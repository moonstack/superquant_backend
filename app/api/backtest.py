from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def test_backtest():
    return {"message": "backtest router is working"}
