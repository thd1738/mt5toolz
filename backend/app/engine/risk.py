from dataclasses import dataclass


@dataclass
class RiskState:
    current_drawdown_pct: float
    daily_pnl: float
    open_trades: int


def can_trade(
    state: RiskState,
    max_trades: int,
    daily_loss_limit: float,
    max_drawdown_pct: float,
) -> tuple[bool, str]:
    if state.open_trades >= max_trades:
        return False, "Max trades reached"
    if state.daily_pnl <= -abs(daily_loss_limit):
        return False, "Daily loss limit reached"
    if state.current_drawdown_pct >= max_drawdown_pct:
        return False, "Max drawdown exceeded"
    return True, "Trading allowed"
