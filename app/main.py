from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import create_db_and_tables, engine, get_session
from app.routes.ats import ats_router
from app.routes.config import config_router
from app.routes.resume import resume_router
from app.services.resume import get_all_resumes, get_resume_dict


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    # Actions on startup
    print("Initializing database and LLM...")
    create_db_and_tables()
    print("Startup complete.")
    yield
    # Actions on shutdown (if any)
    engine.dispose()  # Clean up the engine's connection pool
    print("Shutting down.")


# Mount static files
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Constants
DEFAULT_TAB = "personal"  # Same default as in static/js/app.js

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routes
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(config_router)


@app.get("/", response_class=RedirectResponse)
async def root(session: Session = Depends(get_session)):
    """Redirect from root to the first available resume"""
    try:
        resumes = await get_all_resumes(session)
        if resumes:
            return RedirectResponse(f"/resume/{resumes[0]['id']}")
        else:
            return RedirectResponse("/api/config")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@app.get("/resume/{resume_id}", response_class=HTMLResponse)
async def home(request: Request, resume_id: int, tab: str = Query(None), session: Session = Depends(get_session)):
    resume_data = await get_resume_dict(session, resume_id)

    # Use the same default tab as frontend
    active_tab = tab or DEFAULT_TAB

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "resume_data": resume_data, "active_tab": active_tab},
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
