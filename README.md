# ZeusNxtLvl: AI Trading App

## Project Structure

```text
zeusnxtlvl/
├── backend/                # FastAPI backend code
├── frontend/               # React/Next.js frontend code
├── docker/                 # Dockerfiles and docker-compose.yml
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
├── scripts/                # Deployment and CI scripts
├── .env                    # Environment variables (not committed)
├── README.md               # Project documentation
```

## Launch (Local Docker)

```sh
cd docker && docker-compose up --build -d
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Environment Variables

- All secrets/config must be set in `.env` at the project root.
- No hardcoded secrets in code or Dockerfiles.

## Google Cloud Run

- The Dockerfiles are ready for Cloud Run deployment.
- You may need to adjust environment variables and volumes for production.

## Missing/To-Check

- Ensure `.env` contains all required variables (see backend and database configs).
- If you use CI/CD, add scripts to `/scripts/`.
- If you use static assets or public files for frontend, ensure they are in `/frontend/public/`.
- If you use migrations, add instructions/scripts to `/scripts/`.

---
For more, see `/scripts/README_RESTRUCTURE_CHECKLIST.txt`.

