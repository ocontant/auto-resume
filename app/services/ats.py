import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from sqlalchemy.orm import Session

from app.models import db_resume_to_dict
from app.services.resume import get_resume_by_id

load_dotenv()


async def optimize_resume(session: Session, resume_id: int) -> str:
    resume = await get_resume_by_id(session, resume_id)
    resume_data = db_resume_to_dict(resume)
    prompt = _create_ats_prompt(resume_data)

    system_message = (
        "You are an expert resume writer specializing in creating ATS-optimized resumes. "
        "Focus on keywords, clear formatting, and quantifiable achievements."
    )

    model_name = os.getenv("OPENAI_LLM_MODEL")
    llm = OpenAI(model=model_name, temperature=0.2)

    messages = [ChatMessage(system_message, role=MessageRole.SYSTEM), ChatMessage(prompt, role=MessageRole.USER)]
    response = llm.chat(messages)

    ats_resume_data_html = response.message.content

    clean_ats_resume_data_html = _parse_llm_response(ats_resume_data_html)
    return clean_ats_resume_data_html


def _create_ats_prompt(resume_data: Dict[str, Any]) -> str:
    """Create a prompt for the LLM based on the resume data"""
    resume_json = json.dumps(resume_data, indent=2)

    return f"""
I need you to optimize the following resume to maximize its score on Applicant Tracking Systems (ATS).

## CURRENT RESUME DATA:
{resume_json}

---

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

OUTPUT HTML FORMATED. IT Will be added inside a container. You can use Tailwind for it. Compact spacing
Apply required css to keep html formated
The outer div spacing should keep a small padding only besides font sans
"""


def _parse_llm_response(content: str) -> str:
    content = content.replace("```html", "").replace("```", "")
    return content
