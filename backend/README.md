# Backend (FastAPI + Trading Engine)

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Key endpoints

- `POST /api/v1/connect` - validates MT5 credentials, encrypts password (AES), returns JWT.
- `POST /api/v1/disconnect` - disconnects account.
- `GET /api/v1/dashboard/{login_id}` - account metrics + detected synthetic symbols.
- `POST /api/v1/robot/start` - evaluates strategy mode and risk controls.
- `POST /api/v1/robot/stop` and `POST /api/v1/robot/pause` - robot control.

## Notes

- `MT5Service` is currently an adapter stub to keep the app runnable without a live broker; replace `verify_login`, data feed, and execution functions with direct `MetaTrader5` package calls in deployment.
