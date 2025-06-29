#!/bin/bash
echo "==== GCP DOCKER DEPLOY ===="
docker build -t zeus_nxtlvl:latest .
docker run -d -p 8000:8000 --env-file .env zeus_nxtlvl:latest
