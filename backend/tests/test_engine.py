import pandas as pd

from app.engine.risk import RiskState, can_trade
from app.engine.trading_engine import trading_engine
from app.models.schemas import RiskConfig, TradingMode


def test_can_trade_limits():
    state = RiskState(current_drawdown_pct=12, daily_pnl=-10, open_trades=1)
    allowed, reason = can_trade(state, max_trades=3, daily_loss_limit=50, max_drawdown_pct=10)
    assert not allowed
    assert "drawdown" in reason.lower()


def test_engine_returns_hold_when_risk_blocked():
    df = pd.DataFrame({"close": [1, 2, 3, 4], "high": [1, 2, 3, 4], "low": [1, 2, 3, 4]})
    plan = trading_engine.evaluate(
        mode=TradingMode.scalping,
        risk=RiskConfig(lot_size=0.2, max_trades=1, daily_loss_limit=10, max_drawdown_pct=10),
        market_df=df,
        risk_state=RiskState(current_drawdown_pct=2, daily_pnl=-20, open_trades=0),
    )
    assert plan.action == "HOLD"
    assert plan.reason == "Daily loss limit reached"
