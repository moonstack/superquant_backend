from fastapi import APIRouter, Query
from app.services import backtest_service
from app.core.response import success, error

router = APIRouter(prefix="/backtest", tags=["Backtest"])

@router.get("/historical_data")
async def get_historical_data(
    symbol: str = Query(..., description="股票代码"),
    start_date: str = Query(..., description="开始日期, 格式: YYYYMMDD"),
    end_date: str = Query(..., description="结束日期, 格式: YYYYMMDD"),
    period: str = Query('1m', description="K线周期: 1m, 5m, 30m, 1h, 1d")
):
    try:
        data = backtest_service.get_historical_data(symbol, start_date, end_date, period)
        return data
    except Exception as e:
        return error(str(e))