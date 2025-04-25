from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.ats import optimize_resume

ats_router = APIRouter(prefix="/api/resumes", tags=["ats"])
templates = Jinja2Templates(directory="app/templates")


@ats_router.get("/{resume_id}/optimize")
async def get_optimized_resume(resume_id: int, request: Request, session: Session = Depends(get_session)):
    """Generate an ATS-optimized version of the specified resume"""
    optimized_resume = await optimize_resume(session, resume_id)

    return templates.TemplateResponse(
        "components/ats_preview.html",
        {
            "request": request,
            "optimized_resume": optimized_resume,
        },
    )
