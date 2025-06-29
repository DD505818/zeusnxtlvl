# ZEUS°NXTLVL - THE FINAL SYSTEM

## Install
```bash
pip install -r requirements.txt
```
## Env Config
Copy `.env.example` to `.env` and fill broker, payment, and AI credentials.

## Launch
```bash
bash launch_zeus.sh
# or with Docker
bash deploy_zeus_gcp.sh
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
python backtest.py --agent QuantumBoost --data sample_ohlcv.csv
```
