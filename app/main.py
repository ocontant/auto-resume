from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.models import Resume
from app.routes import resume, ai

# Sample initial data
from app.data import sample_resume

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(resume.router)
app.include_router(ai.router)

# Global state (would be replaced by database in production)
current_resume = sample_resume

# Get current resume data
def get_resume_data():
    return current_resume


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request, resume_data: Resume = Depends(get_resume_data)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume_data": resume_data
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
