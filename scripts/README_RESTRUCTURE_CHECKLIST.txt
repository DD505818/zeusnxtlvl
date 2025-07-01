RESTRUCTURE CHECKLIST (for AI trading app)

- All backend code is in /backend/
- All frontend code is in /frontend/
- All Dockerfiles and docker-compose.yml are in /docker/
- All deployment/CI scripts are in /scripts/
- .env and README.md are at project root
- File names: snake_case for Python, PascalCase for React
- Imports and paths updated for new structure
- /backend/ and /frontend/ each have a correct Dockerfile
- /docker/docker-compose.yml builds and runs backend (8000) and frontend (3000)
- .env is used for secrets/config (no hardcoded secrets)
- README.md documents launch: cd docker && docker-compose up --build -d
- Ready for local Docker and Google Cloud Run deployment

If anything is missing for full stack build/launch, note it in README.md.
