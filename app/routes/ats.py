from fastapi import APIRouter, Depends, Request, Path
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.resume import get_resume_dict
from app.services.ats import optimize_resume

ats_router = APIRouter(prefix="/api/resumes", tags=["ats"])
templates = Jinja2Templates(directory="app/templates")


@ats_router.get("/{resume_id}/optimize")
async def get_optimized_resume(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Generate an ATS-optimized version of the specified resume"""
    resume_data = await get_resume_dict(session, resume_id)
    optimized_resume = await optimize_resume(resume_data)

    return templates.TemplateResponse(
        "components/ats_preview.html",
        {
            "request": request,
            "optimized_resume": optimized_resume,
            "resume_data": resume_data,
        },
    )
