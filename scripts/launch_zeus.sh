#!/bin/bash
set -e
export $(cat .env | xargs)
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
