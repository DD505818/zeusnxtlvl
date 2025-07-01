# ZEUS°NXTLVL - THE FINAL SYSTEM

## Install
```bash
pip install -r requirements.txt
```

## Env Config
Create a `.env` file at the project root (see `.env` for example values).

## Launch with Docker
```bash
cd docker && docker-compose up --build -d
```
## API
- `/trade` — Place trade via broker SDK
- `/deposit/stripe`, `/deposit/paypal` — Initiate fiat deposits
- `/llm/gemini`, `/llm/groq`, `/llm/firecrawl`, `/llm/grok3` — Run LLM agent
- `/ws/all` — Full state WebSocket feed
- `/healthz` — System health
- `/docs` — Full interactive API docs

## Agents
- QuantumBoost, PredictiveProphet, VWAPScalperX, HeikinBreakout, RSIHeikinSniper, GapSniper

## Testing
```bash
python backend/backtest.py --agent QuantumBoost --data sample_ohlcv.csv
```

Scripts for launching locally or on Google Cloud Run are located in the
`scripts/` directory. Example market data (`sample_ohlcv.csv`) is not
provided and should be supplied separately.
