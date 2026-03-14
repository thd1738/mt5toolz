from fastapi import APIRouter, HTTPException

from app.core.security import create_access_token, crypto_service
from app.engine.risk import RiskState
from app.engine.trading_engine import trading_engine
from app.models.schemas import (
    ConnectRequest,
    ConnectResponse,
    DashboardResponse,
    RobotControlRequest,
)
from app.services.mt5_service import mt5_service

router = APIRouter(prefix="/api/v1", tags=["trading-robot"])


@router.post("/connect", response_model=ConnectResponse)
def connect_account(payload: ConnectRequest) -> ConnectResponse:
    if not mt5_service.verify_login(payload.login_id, payload.password, payload.broker_server):
        raise HTTPException(status_code=401, detail="Invalid MT5 credentials")

    user_id = str(payload.login_id)
    mt5_service.connect(user_id, payload.login_id, payload.broker_server)

    encrypted_password = crypto_service.encrypt(payload.password)
    _ = encrypted_password

    token = create_access_token(subject=user_id)
    return ConnectResponse(connected=True, token=token, message="MT5 account connected")


@router.post("/disconnect")
def disconnect_account(login_id: int):
    mt5_service.disconnect(str(login_id))
    return {"disconnected": True}


@router.get("/dashboard/{login_id}", response_model=DashboardResponse)
def get_dashboard(login_id: int) -> DashboardResponse:
    user_id = str(login_id)
    snapshot = mt5_service.account_snapshot(user_id)
    symbols = mt5_service.detect_symbols(user_id)
    return DashboardResponse(**snapshot, symbols=symbols)


@router.post("/robot/start")
def start_robot(payload: RobotControlRequest):
    import numpy as np
    import pandas as pd

    np.random.seed(7)
    closes = 100 + np.cumsum(np.random.normal(0, 0.25, 400))
    highs = closes + np.abs(np.random.normal(0.1, 0.05, 400))
    lows = closes - np.abs(np.random.normal(0.1, 0.05, 400))
    market_df = pd.DataFrame({"close": closes, "high": highs, "low": lows})

    plan = trading_engine.evaluate(
        mode=payload.mode,
        risk=payload.risk,
        market_df=market_df,
        risk_state=RiskState(current_drawdown_pct=3.2, daily_pnl=22.0, open_trades=1),
    )

    return {
        "robot": "started",
        "mode": payload.mode,
        "action": plan.action,
        "lot_size": plan.lot_size,
        "tp_points": plan.take_profit_points,
        "sl_points": plan.stop_loss_points,
        "reason": plan.reason,
    }


@router.post("/robot/stop")
def stop_robot():
    return {"robot": "stopped"}


@router.post("/robot/pause")
def pause_robot():
    return {"robot": "paused"}
