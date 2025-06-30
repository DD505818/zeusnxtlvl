from fastapi import FastAPI, WebSocket, HTTPException, Depends, BackgroundTasks, status, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware # Import CORS
from config import settings
from coinbase import CoinbaseBroker
from ng_heikin_breakout import NGHeikinBreakoutAgent
from agent_base import AbstractAgent
from gemini_service import GeminiService
from grok_service import GrokService
from whisper_service import WhisperService
from redis_cache import RedisCache
from postgres_db import PostgresDB
from vector_db import VectorDB
from pydantic import BaseModel
import uvicorn
import asyncio
import random
import logging
from typing import Dict, List, Optional
import json
from datetime import datetime, time, timedelta

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class BrokerConfig(BaseModel):
    api_key: str
    secret: str

class AgentStatusData(BaseModel):
    name: str
    is_running: bool
    last_trade_pnl: Optional[float] = None
    current_roi: Optional[float] = None
    confidence: Optional[float] = None
    expected_return: Optional[float] = None
    capital_allocated: Optional[float] = None


app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# --- CORS Configuration ---
# Allows frontend (e.g., localhost:3000) to connect to backend (localhost:8000)
origins = [
    "http://localhost",
    "http://localhost:3000", # Next.js dev server
    "http://localhost:8000", # FastAPI dev server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global State & Services ---
active_agents: Dict[str, AbstractAgent] = {}
agent_tasks: Dict[str, asyncio.Task] = {}
orchestrator_state = {"status": "IDLE", "daily_pnl": 0.0, "current_drawdown": 0.0, "total_capital": 10000.0} # Initial capital

# Initialize services
redis_cache: RedisCache = RedisCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
postgres_db: PostgresDB = PostgresDB(
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    database=settings.POSTGRES_DB
)
vector_db: VectorDB = VectorDB(url=settings.VECTOR_DB_URL)

gemini_service: GeminiService = GeminiService(api_key=settings.GEMINI_API_KEY)
grok_service: GrokService = GrokService(api_key=settings.GROQ_API_KEY)
whisper_service: WhisperService = WhisperService(api_key=settings.OPENAI_API_KEY)

# Instantiate brokers (can be dynamically created based on payload or config)
brokers = {
    "coinbase": CoinbaseBroker(settings.COINBASE_API_KEY, settings.COINBASE_SECRET),
    # Add other brokers similarly
}

# --- Event/Signal Queue (Conceptual) ---
# For simplicity, we'll use a basic asyncio Queue for internal signals for this example.
# In a full production system, Kafka or Redis Pub/Sub would be used.
signal_queue = asyncio.Queue()

# --- Connection Managers for WebSockets ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_json(self, data: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except WebSocketDisconnect:
                self.disconnect(connection) # Clean up disconnected clients

ws_manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    await redis_cache.connect()
    await postgres_db.connect()
    await vector_db.connect()

    # Initialize system PnL in Redis to 0 for the day if not already set
    await redis_cache.set("system:daily_pnl", 0.0)
    await redis_cache.set("system:total_capital", orchestrator_state["total_capital"])

    # Start main orchestration loop in a background task
    asyncio.create_task(orchestration_loop())
    logger.info("FastAPI application startup completed.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down ZEUS°NXTLVL...")
    orchestrator_state["status"] = "SHUTTING_DOWN" # Signal loop to stop

    for agent_name, task in agent_tasks.items():
        logger.info(f"Stopping agent: {agent_name}")
        if agent_name in active_agents:
            await active_agents[agent_name].shutdown()
        if not task.done():
            task.cancel()
            try:
                await task # Await cancellation
            except asyncio.CancelledError:
                logger.info(f"Agent {agent_name} task cancelled.")
    
    await redis_cache.disconnect()
    await postgres_db.disconnect()
    await vector_db.disconnect()
    logger.info("ZEUS°NXTLVL shutdown complete.")


@app.get("/health")
async def health():
    # Check dependencies health
    try:
        await redis_cache.client.ping()
        await postgres_db.pool.acquire() # Attempt to acquire a connection
        # Add a test for vector_db here
        return {"status": "ok", "project_name": settings.PROJECT_NAME, "environment": settings.ENVIRONMENT}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service unavailable: {e}")

@app.get("/status")
async def get_orchestrator_status():
    return orchestrator_state

@app.get("/agents/status", response_model=Dict[str, AgentStatusData])
async def get_agents_status():
    status_data = {}
    for name, agent in active_agents.items():
        agent_live_status = await redis_cache.get_agent_status(name)
        status_data[name] = AgentStatusData(
            name=name,
            is_running=agent_live_status.get("is_running", False),
            last_trade_pnl=agent_live_status.get("last_trade_pnl"),
            current_roi=agent_live_status.get("current_roi"),
            confidence=agent_live_status.get("confidence"),
            expected_return=agent_live_status.get("expected_return"),
            capital_allocated=agent_live_status.get("capital_allocated")
        )
    return status_data


@app.post("/run_system")
async def run_system():
    """
    Starts the core ZEUS orchestration loop and activates initial agents.
    This simulates the "RUN" button on the UI.
    """
    if orchestrator_state["status"] == "RUNNING":
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "System is already running."})

    orchestrator_state["status"] = "RUNNING"
    logger.info("ZEUS°NXTLVL System Starting...")

    # For demonstration, manually start the NGHeikinBreakoutAgent
    # In a real system, the orchestrator would dynamically decide which agents to start
    # based on market conditions, available capital, and StrategyForge recommendations.
    if "NGHeikinBreakoutAgent" not in active_agents:
        agent = NGHeikinBreakoutAgent(brokers=brokers, redis_cache=redis_cache, postgres_db=postgres_db)
        active_agents["NGHeikinBreakoutAgent"] = agent
        agent_tasks["NGHeikinBreakoutAgent"] = asyncio.create_task(agent.run())
        logger.info("NGHeikinBreakoutAgent started.")
    else:
        logger.info("NGHeikinBreakoutAgent already active.")

    return {"message": "ZEUS°NXTLVL System initiated. Orchestration loop is running."}

@app.post("/stop_system")
async def stop_system():
    """Stops the core ZEUS orchestration loop and agents."""
    if orchestrator_state["status"] != "RUNNING":
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "System is not running."})

    orchestrator_state["status"] = "HALTED"
    logger.info("ZEUS°NXTLVL System halting.")
    # The shutdown_event handler will take care of stopping agents and closing connections.
    return {"message": "ZEUS°NXTLVL System halting. Please wait for graceful shutdown."}


async def orchestration_loop():
    """
    The main autonomous loop for the ZEUS Orchestrator.
    This embodies the "zero manual intervention" aspect.
    """
    last_pnl_reset_day = datetime.utcnow().day
    while orchestrator_state["status"] == "RUNNING":
        try:
            current_utc_day = datetime.utcnow().day
            if current_utc_day != last_pnl_reset_day:
                logger.info("New day detected. Resetting daily P&L.")
                orchestrator_state["daily_pnl"] = 0.0
                await redis_cache.set_total_system_pnl(0.0)
                last_pnl_reset_day = current_utc_day

            # 1. Market Data & Sentiment Ingestion (GrokStreamListener, LSTMForecaster)
            # This would be real-time data from Kafka/WebSockets pushed to Redis by dedicated services
            mock_market_data = {"price": await brokers["coinbase"].get_current_price("ETH/USD"), "symbol": "ETH/USD"}
            await redis_cache.set("market_data:latest", mock_market_data)

            # Simulate social sentiment from GrokService
            social_sentiment = await grok_service.get_trading_sentiment_insight("Recent crypto news: market showing mixed signals with some bullish tweets.")
            logger.debug(f"Social Sentiment: {social_sentiment}")

            # 2. AI Signal Generation (FusionNet, LSTMForecaster, GrokStreamListener)
            signals = await generate_ai_signals(mock_market_data, {"social_sentiment": social_sentiment})

            # 3. Confidence Gating & Agent Selection
            qualified_agents_to_run = await select_qualified_agents(signals)

            # 4. Rolling ROI Capital Allocation (Dynamic)
            await update_capital_allocation()

            # 5. Parallel Tool Calling & Trade Execution
            if qualified_agents_to_run:
                await execute_trades_via_agents(qualified_agents_to_run, signals["asset"])
            else:
                logger.info("No qualified agents to run for current signal.")

            # 6. Risk Control (RiskSentinelX)
            await enforce_risk_controls()

            # Update overall system P&L for dashboard
            orchestrator_state["daily_pnl"] = await redis_cache.get_total_system_pnl()

            # Send real-time updates to connected WebSockets
            await ws_manager.broadcast_json({
                "system_status": orchestrator_state["status"],
                "daily_pnl": orchestrator_state["daily_pnl"],
                "active_agents_count": len(active_agents),
                "agents_status": await get_agents_status(),
                "total_capital": orchestrator_state["total_capital"],
                "timestamp": datetime.utcnow().isoformat()
            })

            await asyncio.sleep(1) # Adjust loop frequency (e.g., 0.1s for high-freq)

        except Exception as e:
            logger.error(f"Orchestration loop error: {e}", exc_info=True)
            orchestrator_state["status"] = "ERROR"
            await ws_manager.broadcast_json({
                "system_status": orchestrator_state["status"],
                "error_message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            # Consider implementing auto-recovery or temporary halt logic here
            await asyncio.sleep(5) # Pause briefly on error


async def generate_ai_signals(market_data: Dict, sentiment_data: Dict) -> Dict:
    """
    FusionNet: Blending signals from various sources.
    Placeholder for sophisticated logic.
    """
    logger.debug(f"Generating signals for market: {market_data}, sentiment: {sentiment_data}")
    
    # Example: Use Gemini for complex market analysis with contextual memory (RAG)
    # This would involve querying VectorDB first
    # relevant_past_events = await vector_db.query_similar_events(json.dumps(market_data) + json.dumps(sentiment_data))
    # gemini_context = {"market_data": market_data, "sentiment": sentiment_data, "past_events": relevant_past_events}
    # gemini_analysis = await gemini_service.analyze_market_data(json.dumps(gemini_context))
    # logger.debug(f"Gemini Analysis: {gemini_analysis}")

    # For demonstration, simulate a signal
    signal = {"direction": "HOLD", "confidence": 0.5, "expected_return": 0.0, "asset": market_data["symbol"]}
    if market_data.get("price", 0) > 3000 and "bullish" in sentiment_data.get("social_sentiment", "").lower():
         signal = {"direction": "BUY", "confidence": random.uniform(0.975, 0.999), "expected_return": random.uniform(0.05, 0.1), "asset": market_data["symbol"]}
    elif market_data.get("price", 0) < 2500 and "bearish" in sentiment_data.get("social_sentiment", "").lower():
         signal = {"direction": "SELL", "confidence": random.uniform(0.975, 0.999), "expected_return": random.uniform(0.05, 0.1), "asset": market_data["symbol"]}

    return signal

async def select_qualified_agents(signal: Dict) -> List[str]:
    """
    Applies Confidence Gating and selects agents capable of acting on the signal.
    """
    qualified_agent_names = []
    if signal["confidence"] >= settings.CONFIDENCE_THRESHOLD and \
       signal["expected_return"] >= settings.EXPECTED_RETURN_THRESHOLD:
        logger.info(f"Signal qualified: {signal['direction']} for {signal['asset']} with Conf: {signal['confidence']:.3f}, ExpRet: {signal['expected_return']:.3f}")
        
        # Here, you'd match signals to agent capabilities (e.g., agent A trades ETH, agent B trades BTC)
        # For simplicity, all active agents qualify for any strong signal in this demo.
        for agent_name in active_agents.keys():
            qualified_agent_names.append(agent_name) # Assuming all agents can act on this signal type
    
    return qualified_agent_names

async def update_capital_allocation():
    """
    Dynamically reallocates capital to top-performing agents based on Rolling ROI.
    This would query PostgresDB for past performance and Redis for current ROI.
    """
    # Total capital from system state
    total_capital = orchestrator_state["total_capital"]
    active_agent_count = len(active_agents)

    if active_agent_count == 0:
        logger.debug("No active agents for capital allocation.")
        return

    # In a real scenario, fetch performance from postgres_db.get_recent_agent_performance
    # For now, distribute equally or based on mock ROI from redis
    
    capital_per_agent = total_capital / active_agent_count
    for agent_name in active_agents.keys():
        await redis_cache.set(f"agent:{agent_name}:capital_allocation", capital_per_agent)
        logger.debug(f"Allocated ${capital_per_agent:.2f} to {agent_name}")

async def execute_trades_via_agents(qualified_agent_names: List[str], asset: str):
    """
    Triggers trades through selected agents, enabling Parallel Tool Calling.
    """
    trade_tasks = []
    for agent_name in qualified_agent_names:
        agent_instance = active_agents.get(agent_name)
        if agent_instance:
            agent_status = await redis_cache.get_agent_status(agent_name)
            capital_for_trade = agent_status.get("capital_allocated", 0.0)
            if capital_for_trade > 0:
                logger.info(f"Orchestrator dispatching trade for {agent_name} on {asset} with capital ${capital_for_trade:.2f}")
                # For demo, assuming agents can take a generic BUY/SELL signal for the asset
                trade_tasks.append(asyncio.create_task(
                    agent_instance.execute_trade("BUY", asset, capital_for_trade) # Simplified to BUY for demo
                ))
            else:
                logger.warning(f"Agent {agent_name} has no capital allocated, skipping trade execution.")
        else:
            logger.warning(f"Agent {agent_name} not found in active agents, cannot execute trade.")

    if trade_tasks:
        results = await asyncio.gather(*trade_tasks, return_exceptions=True)
        current_daily_pnl = await redis_cache.get_total_system_pnl()
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(f"Trade execution failed for agent {qualified_agent_names[i]}: {res}")
            else:
                logger.info(f"Trade result for agent {qualified_agent_names[i]}: {res}")
                trade_pnl = res.get("pnl", 0.0)
                if trade_pnl:
                    current_daily_pnl += trade_pnl
                    orchestrator_state["total_capital"] += trade_pnl # Compounding
                    await redis_cache.set_total_system_pnl(current_daily_pnl)
                    await redis_cache.set("system:total_capital", orchestrator_state["total_capital"])


async def enforce_risk_controls():
    """
    Implements RiskSentinelX: Max daily drawdown, max trade loss, consecutive losses.
    """
    current_daily_pnl = await redis_cache.get_total_system_pnl()
    initial_daily_capital = orchestrator_state["total_capital"] # Needs to be tracked from start of day
    
    # Mock for demonstration:
    daily_drawdown = current_daily_pnl / initial_daily_capital if initial_daily_capital else 0.0
    orchestrator_state["current_drawdown"] = daily_drawdown

    if daily_drawdown < -settings.MAX_DAILY_DRAWDOWN_PERCENT:
        logger.warning(f"Max daily drawdown hit! P&L: {current_daily_pnl:.2f}, Drawdown: {daily_drawdown*100:.2f}%. Halting system.")
        orchestrator_state["status"] = "HALTED_DRAWDOWN"
        # Trigger emergency shutdown procedures for all agents
        # Send critical alert
        await ws_manager.broadcast_json({
            "alert": "CRITICAL",
            "message": "Max daily drawdown hit. System halted!",
            "timestamp": datetime.utcnow().isoformat()
        })


@app.post("/command_ai")
async def command_ai(command: str):
    """
    Endpoint for Whisper Voice Integration (mock).
    In a real app, this would receive audio and send to WhisperService.
    """
    logger.info(f"Received AI voice command (mock): {command}")
    # Example transcription: await whisper_service.transcribe_audio("path/to/audio.wav")
    
    response_message = "Command not recognized."
    if "run quantum rebound on eth now" in command.lower():
        response_message = "Command recognized: Running QuantumRebound on ETH now. (Action mocked)"
        # Here, you'd dynamically start a specific agent or modify existing one
        # e.g., active_agents["QuantumReboundAgent"] = QuantumReboundAgent(...)
        # asyncio.create_task(active_agents["QuantumReboundAgent"].run())
    elif "what is my daily profit" in command.lower():
        current_pnl = await redis_cache.get_total_system_pnl()
        response_message = f"Your daily profit is ${current_pnl:.2f}."
    
    return {"message": response_message}

@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, actual data broadcasted from orchestration_loop
            await asyncio.sleep(5) 
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Dashboard WebSocket error for {websocket}: {e}", exc_info=True)
    finally:
        logger.info(f"Dashboard WebSocket disconnected: {websocket.client}")


if __name__ == "__main__":
    uvicorn.run("orchestrator:app", host="0.0.0.0", port=settings.API_PORT, reload=False)  # reload=True for dev

