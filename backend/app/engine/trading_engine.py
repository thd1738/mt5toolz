from dataclasses import dataclass

import pandas as pd

from app.engine.risk import RiskState, can_trade
from app.engine.strategies import generate_signal
from app.models.schemas import RiskConfig, TradingMode


@dataclass
class TradePlan:
    action: str
    lot_size: float
    take_profit_points: int
    stop_loss_points: int
    reason: str


class TradingEngine:
    def evaluate(
        self,
        mode: TradingMode,
        risk: RiskConfig,
        market_df: pd.DataFrame,
        risk_state: RiskState,
    ) -> TradePlan:
        allowed, risk_reason = can_trade(
            risk_state,
            max_trades=risk.max_trades,
            daily_loss_limit=risk.daily_loss_limit,
            max_drawdown_pct=risk.max_drawdown_pct,
        )
        if not allowed:
            return TradePlan("HOLD", risk.lot_size, 0, 0, risk_reason)

        signal = generate_signal(mode, market_df)
        if signal.action == "HOLD":
            return TradePlan("HOLD", risk.lot_size, 0, 0, signal.reason)

        tp_sl = {
            TradingMode.ultra_scalping: (60, 120),
            TradingMode.scalping: (200, 300),
            TradingMode.long_trade: (900, 600),
        }[mode]

        return TradePlan(
            action=signal.action,
            lot_size=risk.lot_size,
            take_profit_points=tp_sl[0],
            stop_loss_points=tp_sl[1],
            reason=signal.reason,
        )


trading_engine = TradingEngine()
