#!/bin/bash
echo "==== GCP DOCKER DEPLOY ===="
docker build -f ../docker/backend.Dockerfile -t zeus_nxtlvl_backend ../backend
docker run -d -p 8000:8000 --env-file ../.env zeus_nxtlvl_backend
