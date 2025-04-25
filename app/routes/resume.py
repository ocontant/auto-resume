from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.resume import (
    add_education,
    add_experience,
    add_project,
    delete_education_by_id,
    delete_experience_by_id,
    delete_project_by_id,
    get_resume_by_id,
    get_resume_dict,
    update_education_field,
    update_experience_field,
    update_personal_info,
    update_project_field,
    update_project_point,
    update_skills,
)

resume_router = APIRouter(prefix="/api/resumes", tags=["resume"])
templates = Jinja2Templates(directory="app/templates")


@resume_router.get("/{resume_id}/section/personal")
async def get_personal_section(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Get the personal information section of a specific resume form"""
    resume_data = await get_resume_dict(session, resume_id)
    return templates.TemplateResponse(
        "components/personal_form.html",
        {"request": request, "resume_data": resume_data},
    )


@resume_router.get("/{resume_id}/section/experience")
async def get_experience_section(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Get the experience section of a specific resume form"""
    resume_data = await get_resume_dict(session, resume_id)
    return templates.TemplateResponse(
        "components/resume_form.html", {"request": request, "resume_data": resume_data}
    )


@resume_router.get("/{resume_id}/section/skills")
async def get_skills_section(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Get the skills section of a specific resume form"""
    resume_data = await get_resume_dict(session, resume_id)
    return templates.TemplateResponse(
        "components/skills_form.html", {"request": request, "resume_data": resume_data}
    )


@resume_router.get("/{resume_id}/section/education")
async def get_education_section(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Get the education section of a specific resume form"""
    resume_data = await get_resume_dict(session, resume_id)
    return templates.TemplateResponse(
        "components/education_form.html",
        {"request": request, "resume_data": resume_data},
    )


@resume_router.get("/{resume_id}/section/projects")
async def get_projects_section(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Get the projects section of a specific resume form"""
    resume_data = await get_resume_dict(session, resume_id)
    return templates.TemplateResponse(
        "components/projects_form.html",
        {"request": request, "resume_data": resume_data},
    )


@resume_router.patch("/{resume_id}/personal_info/{field}")
async def update_personal_info_field(
    resume_id: int, field: str, value: str = Form(...), session: Session = Depends(get_session)
):
    """Update a field in the personal info section"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await update_personal_info(session, resume_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume with ID {resume_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@resume_router.patch("/{resume_id}/skills/{field}")
async def update_skills_field_endpoint(
    resume_id: int, field: str, value: str = Form(...), session: Session = Depends(get_session)
):
    """Update a skills field"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await update_skills(session, resume_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume with ID {resume_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@resume_router.patch("/{resume_id}/education/{education_id}/{field}")
async def update_education_field_endpoint(
    resume_id: int,
    education_id: int,
    field: str,
    value: str = Form(...),
    session: Session = Depends(get_session),
):
    """Update a field in an education entry"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await update_education_field(session, resume_id, education_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or education entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@resume_router.patch("/{resume_id}/experience/{experience_id}/{field}")
async def update_experience_field_endpoint(
    resume_id: int,
    experience_id: int,
    field: str,
    value: str = Form(...),
    session: Session = Depends(get_session),
):
    """Update a field in an experience entry"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await update_experience_field(session, resume_id, experience_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or experience entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@resume_router.patch("/{resume_id}/project/{project_id}/{field}")
async def update_project_field_endpoint(
    resume_id: int,
    project_id: int,
    field: str,
    value: str = Form(...),
    session: Session = Depends(get_session),
):
    """Update a project field"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await update_project_field(session, resume_id, project_id, field, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or project not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@resume_router.patch("/{resume_id}/project/{project_id}/point/{point_index}")
async def update_project_point_endpoint(
    resume_id: int,
    project_id: int,
    point_index: int,
    value: str = Form(...),
    session: Session = Depends(get_session),
):
    """Update a project point"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await update_project_point(session, resume_id, project_id, point_index, value)
        return {"value": value}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume, project, or point index not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@resume_router.post("/{resume_id}/education")
async def add_education_endpoint(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Add a new education entry to the resume"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        new_education = await add_education(session, resume_id)
        return templates.TemplateResponse(
            "components/education_item.html", {"request": request, "edu": new_education}
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume with ID {resume_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding education: {str(e)}")


@resume_router.delete("/{resume_id}/education/{education_id}")
async def delete_education_endpoint(resume_id: int, education_id: int, session: Session = Depends(get_session)):
    """Delete an education entry from the resume by its ID."""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await delete_education_by_id(session, resume_id, education_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or education entry not found")
    return Response(content="", status_code=200, media_type="text/plain")


@resume_router.post("/{resume_id}/project")
async def add_project_endpoint(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Add a new project to the resume"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        new_project = await add_project(session, resume_id)
        return templates.TemplateResponse(
            "components/project_item.html", {"request": request, "project": new_project}
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume with ID {resume_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding project: {str(e)}")


@resume_router.delete("/{resume_id}/project/{project_id}")
async def delete_project_endpoint(resume_id: int, project_id: int, session: Session = Depends(get_session)):
    """Delete a project from the resume by its ID."""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await delete_project_by_id(session, resume_id, project_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or project not found")
    return Response(content="", status_code=200, media_type="text/plain")


@resume_router.post("/{resume_id}/experience")
async def add_experience_endpoint(request: Request, resume_id: int, session: Session = Depends(get_session)):
    """Add a new experience entry to the resume"""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        new_experience = await add_experience(session, resume_id)
        return templates.TemplateResponse(
            "components/experience_item.html",
            {"request": request, "item": new_experience},
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume with ID {resume_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding experience: {str(e)}")


@resume_router.delete("/{resume_id}/experience/{experience_id}")
async def delete_experience_endpoint(resume_id: int, experience_id: int, session: Session = Depends(get_session)):
    """Delete an experience entry by its ID."""
    try:
        # Verify resume exists
        await get_resume_by_id(session, resume_id)
        await delete_experience_by_id(session, resume_id, experience_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or experience entry not found")
    return Response(content="", status_code=200, media_type="text/plain")
