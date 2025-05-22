from fastapi import FastAPI
from app.api import factors, backtest, trade

app = FastAPI(title="SuperQuant API")

# 注册路由模块
app.include_router(factors.router)
app.include_router(backtest.router)
app.include_router(trade.router)
