from enum import Enum

from pydantic import BaseModel, Field


class TradingMode(str, Enum):
    ultra_scalping = "ultra_scalping"
    scalping = "scalping"
    long_trade = "long_trade"


class ConnectRequest(BaseModel):
    login_id: int
    password: str
    broker_server: str


class ConnectResponse(BaseModel):
    connected: bool
    token: str
    message: str


class RiskConfig(BaseModel):
    lot_size: float = Field(default=0.2, gt=0)
    max_trades: int = Field(default=3, ge=1)
    daily_loss_limit: float = Field(default=50, gt=0)
    max_drawdown_pct: float = Field(default=10, gt=0)


class RobotControlRequest(BaseModel):
    mode: TradingMode
    risk: RiskConfig


class DashboardResponse(BaseModel):
    balance: float
    equity: float
    open_trades: int
    daily_profit: float
    robot_status: str
    symbols: list[str]
