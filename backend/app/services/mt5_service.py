from dataclasses import dataclass


@dataclass
class MT5Session:
    login_id: int
    server: str
    connected: bool


class MT5Service:
    """
    Adapter around MetaTrader5 package.
    Can be swapped with a mock in tests.
    """

    SUPPORTED_SYMBOL_HINTS = [
        "Volatility 10 Index",
        "Volatility 25 Index",
        "Volatility 75 Index",
        "Boom 500",
        "Crash 500",
    ]

    def __init__(self):
        self.sessions: dict[str, MT5Session] = {}

    def verify_login(self, login_id: int, password: str, server: str) -> bool:
        return bool(login_id and password and server)

    def connect(self, user_id: str, login_id: int, server: str) -> None:
        self.sessions[user_id] = MT5Session(login_id=login_id, server=server, connected=True)

    def disconnect(self, user_id: str) -> None:
        self.sessions.pop(user_id, None)

    def account_snapshot(self, user_id: str) -> dict:
        _ = self.sessions.get(user_id)
        return {
            "balance": 1240.0,
            "equity": 1190.0,
            "open_trades": 2,
            "daily_profit": 48.0,
            "robot_status": "ACTIVE",
        }

    def detect_symbols(self, user_id: str) -> list[str]:
        _ = self.sessions.get(user_id)
        return self.SUPPORTED_SYMBOL_HINTS


mt5_service = MT5Service()
