# ZEUS°NXTLVL

This repository contains a minimal AI trading stack with a FastAPI backend and a
Next.js frontend.

**Note:** Docker and Node.js (v20+) are required in addition to Python 3.12. Be
sure to install the dependencies listed in `backend/requirements.txt` and have a
`sample_ohlcv.csv` available for the backtester (or pass a different file via
`--data`).

## Project Layout
- **backend/** – FastAPI application and trading logic
- **frontend/** – Next.js client
- **docker/** – Dockerfiles and `docker-compose.yml`
- **scripts/** – Deployment and helper scripts
- `.env` – environment variables loaded by the backend

## Quick Start
1. Create a `.env` file based on the keys in `backend/core/config.py`.
2. Build and run the stack:

```bash
cd docker && docker-compose up --build -d
```

The API will be available on `http://localhost:8000` and the frontend on `http://localhost:3000`.

## Development
Run the backtest locally:
```bash
python -m backend.backtest --agent QuantumBoost --data sample_ohlcv.csv
```

Docker must be installed to run `docker-compose`. If Docker is not available,
use the launch script under `scripts/` to run the backend locally after
installing dependencies.

