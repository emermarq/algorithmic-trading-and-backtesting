from fastapi import FastAPI
from app.api.v2 import backtest

app = FastAPI(title="Trading API")

app.include_router(backtest.router, prefix="/backtests/run", tags=["backtest"])