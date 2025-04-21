from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.routes import router as resume_router
from app.db import create_db_and_tables, get_session
from app.services.resume import get_or_create_default_resume

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routes
app.include_router(resume_router)

@app.on_event("startup")
def on_startup():
    # Create database tables on startup
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_session)):
    # Get resume data directly from the service
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume_data": resume_data
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
