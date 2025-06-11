# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AutoResume AI is a self-hosted web application for creating and optimizing resumes for Applicant Tracking Systems (ATS) using AI. It uses FastAPI backend with HTMX+Tailwind frontend, SQLite database, and integrates with OpenAI for AI-powered optimization.

## Common Commands

```bash
# Development
make fix          # Auto-format code (isort → autoflake → black → lint)
make lint         # Run flake8 linting
make test         # Run pytest test suite
make install-dev  # Install development dependencies

# Running the application
docker-compose up -d --build  # Build and run (accessible at http://localhost:8010)
```

## High-Level Architecture

### Directory Structure
- `app/routes/`: FastAPI routers (resume.py, ats.py, config.py)
- `app/services/`: Business logic layer
- `app/templates/`: Jinja2 templates with HTMX
- `app/models.py`: Pydantic models for data validation
- `app/db.py`: SQLAlchemy models and database setup

### Key Patterns
1. **Service Layer Pattern**: Business logic is separated from routes into services
2. **HTMX Endpoints**: Return HTML fragments for dynamic updates without JavaScript
3. **Component Templates**: Reusable template components in `templates/components/`
4. **Database Models**: Resume is the central entity with related PersonalInfo, SkillSet, Experience, Projects, and Education

### Database Schema
- SQLAlchemy ORM with SQLite
- Cascade deletion configured for related entities
- Config table for runtime settings (API keys, models, etc.)

### Frontend Architecture
- HTMX for reactivity (no complex JavaScript framework)
- Tailwind CSS for styling
- Templates use Jinja2 with component-based structure
- Dynamic updates via `hx-*` attributes

### API Design
- RESTful endpoints under `/api/` return JSON
- HTMX endpoints return HTML fragments
- Consistent error handling with FastAPI's HTTPException

## Testing Approach
- Async tests using pytest-asyncio
- Comprehensive fixtures in `conftest.py`
- Mock OpenAI API calls using AsyncMock
- Test files mirror source structure (test_routes_*, test_services_*, etc.)

## Code Style
- Black formatter (115 char line length)
- isort for import sorting
- flake8 for linting
- Type hints throughout the codebase