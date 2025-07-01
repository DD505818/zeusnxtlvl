from fastapi import FastAPI, WebSocket
import uvicorn

from backend.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("connected")
    await ws.close()

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app", host="0.0.0.0", port=settings.API_PORT, reload=False
    )
