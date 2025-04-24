from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import create_db_and_tables, engine, get_session
from app.routes.ats import ats_router
from app.routes.resume import resume_router
from app.services.ats import init_llm
from app.services.resume import get_or_create_default_resume


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    # Actions on startup
    print("Initializing database and LLM...")
    create_db_and_tables()
    init_llm()
    print("Startup complete.")
    yield
    # Actions on shutdown (if any)
    engine.dispose() # Clean up the engine's connection pool
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


# let's keep it here for simplicity
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, tab: str = Query(None), session: Session = Depends(get_session)):
    # Get resume data directly from the service
    resume_data = await get_or_create_default_resume(session)

    # Use the same default tab as frontend
    active_tab = tab or DEFAULT_TAB

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "resume_data": resume_data, "active_tab": active_tab},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)