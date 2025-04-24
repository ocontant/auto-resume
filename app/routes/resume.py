from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.resume import (
    get_or_create_default_resume, add_education, delete_education, add_project,
    delete_project, update_personal_info, update_skills, update_education_field,
    update_experience_field, update_experience_point, update_project_field,
    update_project_point
)

router = APIRouter(prefix="/api/resume", tags=["resume"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/section/personal")
async def get_personal_section(request: Request, session: Session = Depends(get_session)):
    """Get the personal information section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/personal_form.html", {"request": request, "resume_data": resume_data})


@router.get("/section/experience")
async def get_experience_section(request: Request, session: Session = Depends(get_session)):
    """Get the experience section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/resume_form.html", {"request": request, "resume_data": resume_data})


@router.get("/section/skills")
async def get_skills_section(request: Request, session: Session = Depends(get_session)):
    """Get the skills section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/skills_form.html", {"request": request, "resume_data": resume_data})


@router.get("/section/education")
async def get_education_section(request: Request, session: Session = Depends(get_session)):
    """Get the education section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/education_form.html",
                                      {"request": request, "resume_data": resume_data})


@router.get("/section/projects")
async def get_projects_section(request: Request, session: Session = Depends(get_session)):
    """Get the projects section of the resume form"""
    resume_data = await get_or_create_default_resume(session)
    return templates.TemplateResponse("components/projects_form.html", {"request": request, "resume_data": resume_data})


@router.patch("/personal_info/{field}")
async def update_personal_info_field(field: str, value: str = Form(...), session: Session = Depends(get_session)):
    """Update a field in the personal info section"""
    try:
        resume = await get_or_create_default_resume(session)
        await update_personal_info(session, resume["id"], field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Personal info not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/skills/{field}")
async def update_skills_field_endpoint(field: str, value: str = Form(...), session: Session = Depends(get_session)):
    """Update a skills field"""
    try:
        resume = await get_or_create_default_resume(session)
        await update_skills(session, resume["id"], field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Skills not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/education/{education_id}/{field}")
async def update_education_field_endpoint(education_id: int, field: str, value: str = Form(...),
                                          session: Session = Depends(get_session)):
    """Update a field in an education entry"""
    try:
        await update_education_field(session, education_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Education entry with ID {education_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/experience/{experience_id}/{field}")
async def update_experience_field_endpoint(experience_id: int, field: str, value: str = Form(...),
                                           session: Session = Depends(get_session)):
    """Update a field in an experience entry"""
    try:
        await update_experience_field(session, experience_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Experience entry with ID {experience_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/experience/{experience_id}/point/{point_index}")
async def update_experience_point_endpoint(experience_id: int, point_index: int, value: str = Form(...),
                                           session: Session = Depends(get_session)):
    """Update an experience point"""
    try:
        await update_experience_point(session, experience_id, point_index, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Experience entry with ID {experience_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/project/{project_id}/{field}")
async def update_project_field_endpoint(project_id: int, field: str, value: str = Form(...),
                                        session: Session = Depends(get_session)):
    """Update a project field"""
    try:
        resume = await get_or_create_default_resume(session)
        await update_project_field(session, resume["id"], project_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/project/{project_id}/point/{point_index}")
async def update_project_point_endpoint(project_id: int, point_index: int, value: str = Form(...),
                                        session: Session = Depends(get_session)):
    """Update a project point"""
    try:
        resume = await get_or_create_default_resume(session)
        await update_project_point(session, resume["id"], project_id, point_index, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"Project with ID {project_id} not found or point index out of range")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/education")
async def add_education_endpoint(request: Request, session: Session = Depends(get_session)):
    """Add a new education entry to the resume"""
    resume_data = await get_or_create_default_resume(session)
    new_education, index = await add_education(session, resume_data["id"])

    return templates.TemplateResponse("components/education_item.html",
                                      {"request": request, "edu": new_education, "index": index})


@router.delete("/education/{index}")
async def delete_education_endpoint(index: int, session: Session = Depends(get_session)):
    """Delete an education entry from the resume"""
    resume_data = await get_or_create_default_resume(session)
    await delete_education(session, resume_data["id"], index)

    return 200


@router.post("/project")
async def add_project_endpoint(request: Request, session: Session = Depends(get_session)):
    """Add a new project to the resume"""
    resume_data = await get_or_create_default_resume(session)

    new_project, index = await add_project(session, resume_data["id"])

    return templates.TemplateResponse("components/project_item.html",
                                      {"request": request, "project": new_project, "index": index})


@router.delete("/project/{index}")
async def delete_project_endpoint(index: int, session: Session = Depends(get_session)):
    """Delete a project from the resume"""
    resume_data = await get_or_create_default_resume(session)
    await delete_project(session, resume_data["id"], index)

    return ""
