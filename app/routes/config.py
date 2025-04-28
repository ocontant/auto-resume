from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.config import (
    get_ats_settings,
    get_llm_settings,
    get_pdf_page_margin,
    save_ats_settings,
    save_llm_settings,
    save_pdf_page_margin,
)
from app.services.pdf_import import import_resume_from_pdf
from app.services.resume import delete_resume_by_id, get_all_resumes

config_router = APIRouter(prefix="/api/config", tags=["config"])
templates = Jinja2Templates(directory="app/templates")


@config_router.get("")
async def get_config_page(request: Request, session: Session = Depends(get_session)):
    """Render the configuration page."""
    resumes = await get_all_resumes(session)
    job_description, ats_prompt = await get_ats_settings(session)
    api_key, model = await get_llm_settings(session)
    pdf_margin = await get_pdf_page_margin(session)

    return templates.TemplateResponse(
        "config.html",
        {
            "request": request,
            "resumes": resumes,
            "ats_prompt": ats_prompt,
            "job_description": job_description,
            "api_key": api_key,
            "model": model,
            "pdf_margin": pdf_margin,
        },
    )


@config_router.post("/import-resume")
async def import_resume(
    request: Request,
    resume_name: str = Form(...),
    resume_file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    try:
        file_content = await resume_file.read()
        await import_resume_from_pdf(file_content, session, resume_name)

        resumes = await get_all_resumes(session)
        return templates.TemplateResponse(
            "components/resume_list_items.html", {"request": request, "resumes": resumes}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@config_router.delete("/resume/{resume_id}")
async def delete_resume(resume_id: int, session: Session = Depends(get_session)):
    """Delete a resume by ID if it's not the only one."""
    try:
        await delete_resume_by_id(session, resume_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Resume or education entry not found")
    return Response(content="", status_code=200, media_type="text/plain")


@config_router.post("/save-ats-settings")
async def save_ats_settings_endpoint(
    request: Request,
    job_description: str = Form(None),
    ats_prompt: str = Form(...),
    session: Session = Depends(get_session),
):
    """Save ATS optimization settings"""
    try:
        await save_ats_settings(session, job_description, ats_prompt)
        return templates.TemplateResponse(
            "components/settings_feedback.html", {"request": request, "success": True}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "components/settings_feedback.html", {"request": request, "success": False, "error": str(e)}
        )


@config_router.post("/save-llm-settings")
async def save_llm_settings_endpoint(
    request: Request,
    api_key: str = Form(...),
    model: str = Form(...),
    session: Session = Depends(get_session),
):
    """Save LLM settings"""
    try:
        await save_llm_settings(session, api_key, model)
        return templates.TemplateResponse(
            "components/settings_feedback.html", {"request": request, "success": True}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "components/settings_feedback.html", {"request": request, "success": False, "error": str(e)}
        )


@config_router.post("/save-pdf-margin")
async def save_pdf_margin_endpoint(
    request: Request, margin: str = Form(...), session: Session = Depends(get_session)
):
    """Save PDF margin setting"""
    try:
        await save_pdf_page_margin(session, margin)
        return templates.TemplateResponse(
            "components/settings_feedback.html", {"request": request, "success": True}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "components/settings_feedback.html", {"request": request, "success": False, "error": str(e)}
        )
