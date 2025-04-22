from fastapi import APIRouter, Request, Depends, Body
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.ats import optimize_resume
from app.services.resume import get_or_create_default_resume

router = APIRouter(prefix="/api/ats", tags=["ats"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/optimize")
async def get_optimized_resume(
    request: Request,
    session: Session = Depends(get_session)
):
    """Generate an ATS-optimized version of the current resume"""
    resume_data = await get_or_create_default_resume(session)
    optimized_resume = await optimize_resume(resume_data)
    
    return templates.TemplateResponse("components/ats_preview.html", {
        "request": request,
        "optimized_resume": optimized_resume,
        "resume_data": resume_data
    })
