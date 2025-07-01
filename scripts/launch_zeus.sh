#!/bin/bash
echo "==== ZEUS°NXTLVL LAUNCH ===="
export $(cat .env | xargs)
pip install -r ../backend/requirements.txt
uvicorn backend.orchestrator:app --host 0.0.0.0 --port ${API_PORT:-8000} --reload
