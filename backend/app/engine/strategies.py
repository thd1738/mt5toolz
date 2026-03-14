from dataclasses import dataclass

import numpy as np
import pandas as pd

from app.models.schemas import TradingMode


@dataclass
class Signal:
    action: str  # BUY, SELL, HOLD
    reason: str


def _ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    gain_ema = pd.Series(gain, index=series.index).ewm(alpha=1 / period, adjust=False).mean()
    loss_ema = pd.Series(loss, index=series.index).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain_ema / loss_ema.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def ultra_scalping_signal(df: pd.DataFrame) -> Signal:
    ema9 = _ema(df["close"], 9)
    ema21 = _ema(df["close"], 21)
    rsi = _rsi(df["close"]).fillna(50)

    crossed_up = ema9.iloc[-2] <= ema21.iloc[-2] and ema9.iloc[-1] > ema21.iloc[-1]
    crossed_down = ema9.iloc[-2] >= ema21.iloc[-2] and ema9.iloc[-1] < ema21.iloc[-1]

    if crossed_up and rsi.iloc[-1] > 50:
        return Signal("BUY", "EMA9 crossed above EMA21 and RSI > 50")
    if crossed_down and rsi.iloc[-1] < 50:
        return Signal("SELL", "EMA9 crossed below EMA21 and RSI < 50")
    return Signal("HOLD", "No crossover confirmation")


def scalping_signal(df: pd.DataFrame) -> Signal:
    mid = df["close"].rolling(20).mean()
    std = df["close"].rolling(20).std().fillna(0)
    upper = mid + (2 * std)
    lower = mid - (2 * std)
    rsi = _rsi(df["close"]).fillna(50)
    price = df["close"].iloc[-1]

    if price <= lower.iloc[-1] and rsi.iloc[-1] < 30:
        return Signal("BUY", "Lower Bollinger touch + RSI oversold")
    if price >= upper.iloc[-1] and rsi.iloc[-1] > 70:
        return Signal("SELL", "Upper Bollinger touch + RSI overbought")
    return Signal("HOLD", "No Bollinger reversal setup")


def long_trade_signal(df: pd.DataFrame) -> Signal:
    ema50 = _ema(df["close"], 50)
    ema200 = _ema(df["close"], 200)
    recent_high = df["high"].rolling(20).max().iloc[-2]
    recent_low = df["low"].rolling(20).min().iloc[-2]
    close = df["close"].iloc[-1]

    if ema50.iloc[-1] > ema200.iloc[-1] and close > recent_high:
        return Signal("BUY", "Uptrend + breakout confirmation")
    if ema50.iloc[-1] < ema200.iloc[-1] and close < recent_low:
        return Signal("SELL", "Downtrend + breakdown confirmation")
    return Signal("HOLD", "No trend breakout setup")


def generate_signal(mode: TradingMode, df: pd.DataFrame) -> Signal:
    if mode == TradingMode.ultra_scalping:
        return ultra_scalping_signal(df)
    if mode == TradingMode.scalping:
        return scalping_signal(df)
    return long_trade_signal(df)
