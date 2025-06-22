## Description

This PR adds a professional Docker setup, comprehensive backend documentation, and a robust API for AI-powered Turing Tumble challenge solving. It also introduces a project structure guide and a PR template for future contributions.

## Key Changes

- Added a multi-stage, production-ready Dockerfile for the backend.
- Added a docker-compose.yml for easy orchestration and environment management.
- Created a .env template for secure API key management.
- Updated and expanded the backend README with clear instructions, API reference, and Docker usage.
- Added Docs/PROJECT_STRUCTURE.md to explain the backend codebase and file responsibilities.
- Added a professional PR template in .github/PULL_REQUEST_TEMPLATE.md.
- Improved backend code structure and documentation for maintainability and onboarding.

## Type of change

- [ ] New feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation update

## Checklist

- [x] Backend runs in Docker and locally
- [x] API endpoint returns solved board and metrics
- [x] Documentation is clear and up to date
- [x] PR template is present for future contributions
- [ ] My code follows the project style and guidelines
- [ ] I have added/updated tests if needed
- [ ] I have updated the README/documentation as needed
- [ ] I have tested the changes locally

## How to test

1. Build and run the backend with Docker Compose:
   ```
   docker-compose up --build
   ```
2. Test the API endpoint:
   ```
   curl -X POST http://localhost:8000/api/solve_challenge -H "Content-Type: application/json" -d '{"challenge_id": "01"}'
   ```
3. Review the documentation in TTG_Backend/README.md and TTG_Backend/Docs/PROJECT_STRUCTURE.md.

## Related issues

Closes #85 and #101 