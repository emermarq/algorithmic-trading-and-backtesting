from pydantic import BaseModel
from datetime import datetime

class BacktestRequest(BaseModel):
    ticker: str
    start: str
    end: str
    cash: float = 10000.0

class BacktestResponse(BaseModel):
    id: int
    ticker: str
    start: str
    end: str
    initial_cash: float
    final_value: float
    profit: float
    return_pct: float
    created_at: datetime

    model_config = {
        "from_attributes": True  # Substitui orm_mode
    }


