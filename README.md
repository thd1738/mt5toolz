# MT5 Mobile Trading Robot (iOS-first)

This repository implements a production-style scaffold for a mobile trading robot platform:

```text
Mobile App (Flutter iOS-first)
      ↓
Secure API (FastAPI + JWT + AES)
      ↓
Cloud Trading Engine (Python, pandas, numpy)
      ↓
MetaTrader5 API adapter
      ↓
Broker Server
```

## What is included

- **Mobile app (Flutter):** login screen, account connect flow, dashboard, robot controls (start/stop/pause), mode selection.
- **Backend API (FastAPI):**
  - MT5 connect/disconnect endpoints.
  - Dashboard endpoint showing balance/equity/open trades/daily P&L/robot status.
  - Robot control endpoints.
  - AES encryption utility for MT5 password handling.
  - JWT issuance for authenticated sessions.
- **Trading engine:**
  - `ultra_scalping` (EMA 9/21 crossover + RSI, M1 concept).
  - `scalping` (Bollinger reversal + RSI, M5 concept).
  - `long_trade` (EMA 50/200 + breakout, M30-H1 concept).
  - Risk controls: lot size, max trades, daily loss limit, max drawdown stop.
- **Markets support:** symbol auto-detection list includes Deriv synthetic indices (`Volatility 10/25/75`, `Boom 500`, `Crash 500`) via MT5 service adapter.

## Project layout

- `mobile/` Flutter client app.
- `backend/` FastAPI service and cloud trading engine.

## Backend quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Mobile quick start

```bash
cd mobile
flutter pub get
flutter run -d ios
```

## Security approach

- MT5 credentials are encrypted with **AES** before storage/processing in backend workflow.
- API session uses **JWT** tokens.
- API designed for deployment behind TLS (`https`) on AWS or DigitalOcean VPS.

## Step-by-step runtime flow

1. User installs iOS app.
2. User inputs MT5 login ID, password, and broker server.
3. App sends credentials to secure backend API.
4. Backend verifies/connects through MT5 adapter.
5. Trading engine continuously analyzes market data.
6. Engine emits signal and executes BUY/SELL with TP/SL/lot sizing.
7. Trade appears in MT5 account.
8. Robot manages positions until exit or risk-stop rules trigger.

## Deployment notes

- Use PostgreSQL for persistent users/sessions/trade logs.
- Run API + engine worker on AWS EC2 or DigitalOcean droplet.
- Replace current `MT5Service` stub calls with direct `MetaTrader5` package integration for live execution.
