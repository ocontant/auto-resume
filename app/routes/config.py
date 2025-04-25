from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.pdf_import import import_resume_from_pdf
from app.services.resume import delete_resume_by_id, get_all_resumes

config_router = APIRouter(prefix="/api/config", tags=["config"])
templates = Jinja2Templates(directory="app/templates")


@config_router.get("")
async def get_config_page(request: Request, session: Session = Depends(get_session)):
    """Render the configuration page."""
    resumes = await get_all_resumes(session)
    return templates.TemplateResponse("config.html", {"request": request, "resumes": resumes})


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
        return templates.TemplateResponse("components/resume_list.html", {"request": request, "resumes": resumes})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@config_router.delete("/resume/{resume_id}")
async def delete_resume(resume_id: int, session: Session = Depends(get_session)):
    """Delete a resume by ID if it's not the only one."""
    try:
        await delete_resume_by_id(session, resume_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Resume or education entry not found")
    return Response(content="", status_code=200, media_type="text/plain")
