from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from weasyprint import HTML

from app.db import get_session
from app.services.ats import optimize_resume
from app.services.resume import get_resume_by_id

ats_router = APIRouter(prefix="/api/resumes", tags=["ats"])
templates = Jinja2Templates(directory="app/templates")


HTML_TO_PDF_BASE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Resume</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
        }}
    </style>
</head>
<body>{html_content}</body>
</html>
"""


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


@ats_router.post("/{resume_id}/download-ats-pdf")
async def download_ats_resume_pdf_from_html(
    resume_id: int, html_content: str = Form(...), session: Session = Depends(get_session)
):
    """Generate and download the ATS-optimized version of the resume as PDF from provided HTML."""
    try:
        resume = await get_resume_by_id(session, resume_id)
        full_html = HTML_TO_PDF_BASE.format(html_content=html_content)
        pdf_bytes = HTML(string=full_html).write_pdf()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment;filename=optimized_resume_{resume.name}.pdf"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
