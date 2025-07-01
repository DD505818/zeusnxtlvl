# ZEUS°NXTLVL - THE FINAL SYSTEM

> **Note**: The frontend is a minimal placeholder and may require `npm install` during Docker build. Ensure your `.env` contains valid API keys before launching.

## Install
```bash
pip install -r backend/requirements.txt
```
## Env Config
Copy `.env.example` to `.env` and fill broker, payment, and AI credentials.

## Launch
```bash
cd docker && docker-compose up --build -d
```

Run backend locally with Uvicorn:
```bash
uvicorn backend.orchestrator:app --host 0.0.0.0 --port 8000
```
## API
- `/trade` — Place trade via broker SDK
- `/deposit/stripe`, `/deposit/paypal` — Initiate fiat deposits
- `/llm/gemini`, `/llm/groq`, `/llm/firecrawl`, `/llm/grok3` — Run LLM agent
 - `/ws/all` — Full state WebSocket feed
 - `/health` — System health
- `/docs` — Full interactive API docs

## Agents
- QuantumBoost, PredictiveProphet, VWAPScalperX, HeikinBreakout, RSIHeikinSniper, GapSniper

## Testing
```bash
python backtest.py --agent QuantumBoost --data sample_ohlcv.csv
```
