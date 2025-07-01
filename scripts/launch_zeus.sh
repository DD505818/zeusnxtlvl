#!/bin/bash
echo "==== ZEUS°NXTLVL LAUNCH ===="
export $(cat .env | xargs)
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
