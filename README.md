# ZEUS°NXTLVL

This repository contains a minimal AI trading stack with a FastAPI backend and a Next.js frontend.
**Note:** Docker, Node.js, and Python 3.12 must be available to build the containers. Install the packages in `backend/requirements.txt` and provide a `sample_ohlcv.csv` file for backtesting or adjust the `--data` argument.

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

