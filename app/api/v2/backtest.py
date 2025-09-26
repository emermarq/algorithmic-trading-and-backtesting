from fastapi import APIRouter, HTTPException, Depends, Query, Path
from app.schemas.backtest import BacktestRequest, BacktestResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.backtest import run_backtest_and_save

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BacktestResponse, summary="Executa e salva um backtest")
async def backtest(request: BacktestRequest, db: Session = Depends(get_db)):
    result = run_backtest_and_save(
        db=db,
        ticker=request.ticker,
        start=request.start,
        end=request.end,
        cash=request.cash
    )
    if not result:
        raise HTTPException(status_code=400, detail=f"Nenhum dado encontrado para {request.ticker}")
    return result