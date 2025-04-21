from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.resume_service import get_or_create_default_resume

router = APIRouter(prefix="/api/resume", tags=["resume"])

# Templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/section/personal")
async def get_personal_section(request: Request, session: Session = Depends(get_session)):
    """Get the personal information section of the resume form"""
    resume_data = get_or_create_default_resume(session)
    return templates.TemplateResponse("components/personal_form.html", {
        "request": request,
        "resume_data": resume_data
    })

@router.get("/section/experience")
async def get_experience_section(request: Request, session: Session = Depends(get_session)):
    """Get the experience section of the resume form"""
    resume_data = get_or_create_default_resume(session)
    return templates.TemplateResponse("components/resume_form.html", {
        "request": request,
        "resume_data": resume_data
    })

@router.get("/section/skills")
async def get_skills_section(request: Request, session: Session = Depends(get_session)):
    """Get the skills section of the resume form"""
    resume_data = get_or_create_default_resume(session)
    return templates.TemplateResponse("components/skills_form.html", {
        "request": request,
        "resume_data": resume_data
    })

@router.get("/section/education")
async def get_education_section(request: Request, session: Session = Depends(get_session)):
    """Get the education section of the resume form"""
    resume_data = get_or_create_default_resume(session)
    return templates.TemplateResponse("components/education_form.html", {
        "request": request,
        "resume_data": resume_data
    })


@router.get("/section/projects")
async def get_projects_section(request: Request, session: Session = Depends(get_session)):
    """Get the projects section of the resume form"""
    resume_data = get_or_create_default_resume(session)
    return templates.TemplateResponse("components/projects_form.html", {
        "request": request,
        "resume_data": resume_data
    })
