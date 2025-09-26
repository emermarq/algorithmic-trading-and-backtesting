from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class BacktestResult(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=True)
    start = Column(String, nullable=True)
    end = Column(String, nullable=True)
    initial_cash = Column(Float, nullable=True)
    final_value = Column(Float, nullable=True)
    profit = Column(Float, nullable=True)
    return_pct = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
