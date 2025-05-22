from fastapi import APIRouter
from app.core.response import success

router = APIRouter(prefix="/api/factors", tags=["因子设置"])

@router.get("/templates")
async def list_templates():
    return success([])

@router.get("/template/{template_id}")
async def get_template(template_id: str):
    return success({})

@router.post("/template")
async def save_template():
    return success()

@router.delete("/template/{template_id}")
async def delete_template(template_id: str):
    return success()
