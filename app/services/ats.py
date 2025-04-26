import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from sqlalchemy.orm import Session

from app.models import db_resume_to_dict
from app.services.resume import get_resume_by_id
from app.services.config import get_ats_settings

load_dotenv()


async def get_default_ats_prompt() -> str:
    """Get the default ATS prompt template"""
    return """
I need you to optimize the following resume to maximize its score on Applicant Tracking Systems (ATS).

## CURRENT RESUME DATA:
{resume_json}

## JOB DESCRIPTION (IF PROVIDED):
{job_description}

---

## OPTIMIZATION INSTRUCTIONS:
1. Add relevant industry keywords based on the skills and experience shown
2. Use active voice and strong action verbs to begin bullet points
3. Quantify achievements where possible (%, $, numbers)
4. Standardize section headings to be ATS-friendly
5. Ensure consistent formatting of dates and locations
6. Focus on relevant skills and experiences
7. IMPORTANT: DO NOT ADD FICTIONAL INFORMATION OR MAKE UP DETAILS - only reword and enhance what already exists
8. Restructure information to highlight strengths

## STRICT REQUIREMENTS:
- NEVER create fictional experience, skills, or projects that don't exist in the input resume
- DO NOT modify fundamental details like names, companies, education institutions
- Maintain all existing projects, experiences, and education entries
- Only enhance wording, formatting, and keyword placement based on ACTUAL resume content
- If job description is provided, tailor keywords and highlights to match, but NEVER invent new experiences

OUTPUT HTML FORMATTED. It will be added inside a container. You can use Tailwind for it. Compact spacing.
Apply required css to keep html formatted.
The outer div spacing should keep a small padding only besides font sans.
"""


async def optimize_resume(session: Session, resume_id: int) -> str:
    resume = await get_resume_by_id(session, resume_id)
    resume_data = await db_resume_to_dict(resume)

    job_description, ats_prompt = await get_ats_settings(session)

    ats_prompt = await build_ats_prompt(resume_data, job_description, ats_prompt)

    system_message = (
        "You are an expert resume writer specializing in creating ATS-optimized resumes. "
        "Focus on keywords, clear formatting, and quantifiable achievements. "
        "Never include fictional information not present in the original resume."
    )

    model_name = os.getenv("OPENAI_LLM_MODEL")
    llm = OpenAI(model=model_name, temperature=0.1)  # Lower temperature for more factual responses

    messages = [ChatMessage(system_message, role=MessageRole.SYSTEM), ChatMessage(ats_prompt, role=MessageRole.USER)]
    response = await llm.achat(messages)

    ats_resume_data_html = response.message.content

    clean_ats_resume_data_html = _parse_llm_response(ats_resume_data_html)
    return clean_ats_resume_data_html


async def build_ats_prompt(resume_data: Dict[str, Any], ats_prompt: str, job_description: str) -> str:
    """Create a prompt for the LLM based on the resume data"""
    resume_json = json.dumps(resume_data, indent=2)
    return ats_prompt.format(
        resume_json=resume_json,
        job_description=job_description
    )


def _parse_llm_response(content: str) -> str:
    content = content.replace("```html", "").replace("```", "")
    return content
