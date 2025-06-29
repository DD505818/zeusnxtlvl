# ZEUS°NXTLVL Trading Logic Deep Dive

This document describes the end-to-end logic flow for autonomous trading in the ZEUS system.

---

## 1. High-Level Architecture

- **Strategy Engine** (`alpha/`): Generates trade signals using rules or ML.
- **Risk Management** (`risk/`): Approves/rejects signals based on exposure, limits, and safety.
- **Order Execution** (`execution/`): Places or simulates trades, handles slippage and fills.
- **Portfolio Management** (`portfolio/`): Updates positions, PnL, and trade history.
- **Integration Layer** (`ingestion/`, `integrations.py`): Connects to market data and broker/exchange APIs.
- **API** (`main.py`, `api/`): Exposes endpoints for trade, metrics, and control.

---

## 2. Trade Flow Overview

1. **Market Data Ingestion**
   - Data from exchanges via WebSockets or REST is received by ingestion modules.
   - Data is parsed into a standard format and passed to the strategy engine.

2. **Signal Generation (Strategy)**
   - Each enabled strategy receives the market data.
   - The strategy outputs a signal: `buy`, `sell`, or `hold` (with confidence/size if needed).
   - Example (Python):
     ```python
     signal = strategy.generate_signal([bar], portfolio, None)
     ```

3. **Risk Check**
   - The risk module evaluates the signal.
   - Checks include exposure, position limits, historical PnL, and kill-switches.
   - If the check fails, the trade is blocked and logged.
     ```python
     if not risk.check_trade(signal, portfolio):
         logging.warning("RiskSentinel blocked trade: %s", signal)
         return
     ```

4. **Order Execution**
   - On approval, the execution module:
     - In **backtest mode**: Simulates fills (with slippage, latency, etc.).
     - In **live mode**: Places orders via broker APIs (e.g., using ccxt).
   - Handles order confirmation, error retries, and partial fills.

5. **Portfolio Update**
   - After execution, the portfolio is updated:
     - Positions, realized/unrealized PnL, and trade logs are adjusted.
     ```python
     portfolio.update(executed_trade)
     ```

6. **Logging & Monitoring**
   - All events (signals, executions, errors) are logged.
   - Metrics are exposed via API endpoints for dashboards and monitoring.

---

## 3. Code Snippet Examples

### Strategy Example

```python
class MomentumStrategy:
    def generate_signal(self, bars, portfolio, context):
        # Simple momentum: buy if price up, sell if price down
        if bars[-1]['close'] > bars[-2]['close']:
            return {"action": "buy", "symbol": bars[-1]['symbol'], "qty": 1}
        elif bars[-1]['close'] < bars[-2]['close']:
            return {"action": "sell", "symbol": bars[-1]['symbol'], "qty": 1}
        else:
            return {"action": "hold"}
```

### Risk Check Example

```python
class RiskManager:
    def check_trade(self, signal, portfolio):
        # Example: block if position size exceeds max
        max_position = 10
        symbol = signal["symbol"]
        if abs(portfolio.positions.get(symbol, 0) + signal.get("qty", 0)) > max_position:
            return False
        return True
```

### Order Execution Example

```python
class OrderExecutor:
    async def handle_signal(self, signal, market_data):
        if not self.risk.check_trade(signal, self.portfolio):
            logging.warning("RiskSentinel blocked trade: %s", signal)
            return
        executed = await self.simulate_fill(signal, market_data)
        if executed:
            self.portfolio.update(executed)
```

### Portfolio Tracking Example

```python
class PortfolioTracker:
    def __init__(self):
        self.positions = {}
        self.trades = []
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0

    def update(self, trade):
        symbol = trade["symbol"]
        qty = trade["qty"]
        price = trade["price"]
        action = trade["action"]
        # Update positions and record trade
        if action == "buy":
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
        elif action == "sell":
            self.positions[symbol] = self.positions.get(symbol, 0) - qty
        self.trades.append(trade)
```

---

## 4. End-to-End Example (Backtest Loop)

```python
for bar in historical_data:
    signal = strategy.generate_signal([bar], portfolio, None)
    if risk.check_trade(signal, portfolio):
        executed = executor.simulate_fill(signal, bar)
        if executed:
            portfolio.update(executed)
```

---

## 5. API Endpoint for Live Trade

```python
@app.post("/trade")
async def execute_trade(trade_request: TradeRequest, current_user: User = Depends(get_current_active_user)):
    # Receives trade request, runs strategy and risk, sends to execution
    ...
```

---

## 6. Extending Logic

- Add new strategies by subclassing and registering in `alpha/`.
- Plug in alternative risk modules (e.g., Value-at-Risk, ML-based).
- Integrate new exchanges by adding to the ingestion/integrations layer.
- Expose additional analytics via API/dashboard.

---

## 7. Monitoring and Safety

- Use `/health` and `/metrics` endpoints to monitor system status.
- All trades and critical events are logged.
- Kill-switch or emergency stop logic is implemented in risk layer.

---

## 8. References

- [FastAPI](https://fastapi.tiangolo.com/)
- [ccxt](https://github.com/ccxt/ccxt) (multi-exchange crypto trading library)
- [Docker Compose](https://docs.docker.com/compose/)
- [Pandas, numpy, scikit-learn, xgboost] for data and modeling

---

**Ready for live and research trading at scale!**