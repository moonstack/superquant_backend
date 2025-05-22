from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def test_factors():
    return {"message": "factors router is working"}
