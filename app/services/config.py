import os
from typing import Optional

from sqlalchemy.orm import Session

from app.db import Config

# Constants for config keys
JOB_DESCRIPTION_KEY = "job_description"
ATS_PROMPT_KEY = "ats_prompt"
OPENAI_API_KEY_KEY = "openai_api_key"
OPENAI_MODEL_KEY = "openai_model"
PDF_PAGE_MARGIN_KEY = "pdf_page_margin"

DEFAULT_PDF_PAGE_MARGIN = "10mm"


async def get_default_ats_prompt() -> str:
    """Get the default ATS prompt template"""
    return """
I need you to optimize the following resume to maximize its score on Applicant Tracking Systems (ATS).

## OPTIMIZATION INSTRUCTIONS:
1. Add relevant industry keywords based on the skills and experience shown
2. Use active voice and strong action verbs to begin bullet points
3. Quantify achievements where possible (%, $, numbers)
4. Standardize section headings to be ATS-friendly
5. Ensure consistent formatting of dates and locations
6. Focus on relevant skills and experiences
7. DO NOT add fictional information - only enhance what exists
8. Restructure information to highlight strengths

## IMPORTANT REQUIREMENTS:
- Do not modify fundamental details like names, companies, education institutions
- Maintain all projects, experiences, and education entries
- Enhance descriptions with industry-specific terminology
- Ensure formatting is clean and consistent

OUTPUT HTML FORMATED. It Will be added inside a container. Compact spacing
Apply required inline css to keep html formated
Do not output other info than the resume html
Font must be sans

RESULT MUST BE FORMATTED WITH PURE HTML AND CSS
ONLY PURE CSS AND HTML ARE ALLOWED
CSS STYLES MUST BE INLINE
"""


async def get_config_value(session: Session, key: str, default: Optional[str]) -> str:
    """Get a configuration value by key"""
    config_entry = session.query(Config).filter(Config.key == key).first()
    if config_entry:
        if value := str(config_entry.value):
            return value
    return default


async def set_config_value(
    session: Session, key: str, value: Optional[str], description: Optional[str] = None
) -> None:
    """Set a configuration value by key"""
    config_entry = session.query(Config).filter(Config.key == key).first()
    if config_entry:
        config_entry.value = value
    else:
        config_entry = Config(key=key, value=value, description=description)
        session.add(config_entry)
    session.commit()


async def get_ats_settings(session: Session) -> (str, str):
    """Get ATS optimization settings"""
    default_ats_prompt = await get_default_ats_prompt()
    ats_prompt = await get_config_value(session, ATS_PROMPT_KEY, default_ats_prompt)
    job_description = await get_config_value(session, JOB_DESCRIPTION_KEY, "No job description provided.")
    return job_description, ats_prompt


async def save_ats_settings(session: Session, job_description: Optional[str], ats_prompt: str) -> None:
    """Save ATS optimization settings"""
    await set_config_value(session, JOB_DESCRIPTION_KEY, job_description, "Job description for ATS optimization")
    await set_config_value(session, ATS_PROMPT_KEY, ats_prompt, "Custom ATS optimization prompt")


async def get_llm_settings(session: Session) -> tuple[str, str]:
    """Get LLM settings (API key and model)"""
    api_key = await get_config_value(session, OPENAI_API_KEY_KEY, os.getenv("OPENAI_API_KEY", ""))
    model = await get_config_value(session, OPENAI_MODEL_KEY, os.getenv("OPENAI_LLM_MODEL", "gpt-3.5-turbo"))
    return api_key, model


async def save_llm_settings(session: Session, api_key: str, model: str) -> None:
    """Save LLM settings"""
    await set_config_value(session, OPENAI_API_KEY_KEY, api_key, "OpenAI API Key for LLM integration")
    await set_config_value(session, OPENAI_MODEL_KEY, model, "OpenAI model for resume optimization")


async def get_pdf_page_margin(session: Session) -> str:
    """Get PDF page margin setting"""
    return await get_config_value(session, PDF_PAGE_MARGIN_KEY, DEFAULT_PDF_PAGE_MARGIN)


async def save_pdf_page_margin(session: Session, margin: str) -> None:
    """Save PDF page margin setting"""
    await set_config_value(session, PDF_PAGE_MARGIN_KEY, margin, "Margin for PDF exports")
