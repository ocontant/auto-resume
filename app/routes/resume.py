from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_session 
from app.services.resume import (
    get_or_create_default_resume, add_education, delete_education,
    add_project, delete_project
)


router = APIRouter(prefix="/api/resume", tags=["resume"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/section/personal")
async def get_personal_section(request: Request, session: Session = Depends(get_session)):
    """Get the personal information section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/personal_form.html", {
        "request": request,
        "resume_data": resume_data
    })

@router.get("/section/experience")
async def get_experience_section(request: Request, session: Session = Depends(get_session)):
    """Get the experience section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/resume_form.html", {
        "request": request,
        "resume_data": resume_data
    })

@router.get("/section/skills")
async def get_skills_section(request: Request, session: Session = Depends(get_session)):
    """Get the skills section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/skills_form.html", {
        "request": request,
        "resume_data": resume_data
    })

@router.get("/section/education")
async def get_education_section(request: Request, session: Session = Depends(get_session)):
    """Get the education section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/education_form.html", {
        "request": request,
        "resume_data": resume_data
    })


@router.get("/section/projects")
async def get_projects_section(request: Request, session: Session = Depends(get_session)):
    """Get the projects section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/projects_form.html", {
        "request": request,
        "resume_data": resume_data
    })


@router.post("/education")
async def add_education_endpoint(request: Request, session: Session = Depends(get_session)):
    """Add a new education entry to the resume"""
    resume_data = await get_or_create_default_resume(session)
    new_education, index = await add_education(session, resume_data["id"])
    
    return templates.TemplateResponse("components/education_item.html", {
        "request": request,
        "edu": new_education,
        "index": index
    })

@router.delete("/education/{index}")
async def delete_education_endpoint(index: int, session: Session = Depends(get_session)):
    """Delete an education entry from the resume"""
    resume_data = await get_or_create_default_resume(session)
    await delete_education(session, resume_data["id"], index)

    return 200

# Project endpoints
@router.post("/project")
async def add_project_endpoint(request: Request, session: Session = Depends(get_session)):
    """Add a new project to the resume"""
    resume_data = await get_or_create_default_resume(session)
    
    new_project, index = await add_project(session, resume_data["id"])
    
    return templates.TemplateResponse("components/project_item.html", {
        "request": request,
        "project": new_project,
        "index": index
    })

@router.delete("/project/{index}")
async def delete_project_endpoint(index: int, session: Session = Depends(get_session)):
    """Delete a project from the resume"""
    resume_data = await get_or_create_default_resume(session)
    await delete_project(session, resume_data["id"], index)

    return ""

@router.patch("/project/{index}/{field}")
async def update_project_field(
    index: int, 
    field: str, 
    value: str = Form(...),
    session: Session = Depends(get_session)
):
    """Update a field in a project"""
    resume_data = await get_or_create_default_resume(session)
    
    if 0 <= index < len(resume_data["projects"]):
        project = resume_data.projects[index]
        
        setattr(project, field, value)
        session.commit()
        
    return value
