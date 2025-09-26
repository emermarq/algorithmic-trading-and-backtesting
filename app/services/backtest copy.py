import backtrader as bt
import yfinance as yf
from sqlalchemy.orm import Session
from app.db.models.backtest import BacktestResult
from datetime import datetime


class SmaCross(bt.Strategy):
    params = dict(pfast=10, pslow=30)

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()

def run_backtest_and_save(db: Session, ticker: str, start: str, end: str, cash: float):
    data = yf.download(ticker, start=start, end=end)
    if data is None or data.empty:
        return None

    datafeed = bt.feeds.PandasData(dataname=data)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.adddata(datafeed)
    cerebro.broker.set_cash(cash)

    start_value = cerebro.broker.getvalue()
    cerebro.run()
    end_value = cerebro.broker.getvalue()

    # start_value = 1000
    # end_value = 2000

    result = BacktestResult(
        id=1,
        ticker=ticker,
        start=start,
        end=end,
        initial_cash=start_value,
        final_value=end_value,
        profit=round(end_value - start_value, 2),
        return_pct=round(((end_value - start_value) / start_value) * 100, 2)
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
