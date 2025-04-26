import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from sqlalchemy.orm import Session

from app.models import db_resume_to_dict
from app.services.config import get_ats_settings
from app.services.resume import get_resume_by_id

load_dotenv()


async def optimize_resume(session: Session, resume_id: int) -> str:
    resume = await get_resume_by_id(session, resume_id)
    resume_data = await db_resume_to_dict(resume)

    job_description, ats_prompt = await get_ats_settings(session)

    user_message = await build_user_message(resume_data, job_description)

    model_name = os.getenv("OPENAI_LLM_MODEL")
    llm = OpenAI(model=model_name, temperature=0.1)  # Lower temperature for more factual responses

    messages = [ChatMessage(ats_prompt, role=MessageRole.SYSTEM), ChatMessage(user_message, role=MessageRole.USER)]
    response = await llm.achat(messages)

    ats_resume_data_html = response.message.content

    clean_ats_resume_data_html = _parse_llm_response(ats_resume_data_html)
    return clean_ats_resume_data_html


async def build_user_message(resume_data: Dict[str, Any], job_description: str) -> str:
    """Create a simple user message with resume data and job description"""
    resume_json = json.dumps(resume_data, indent=2)

    user_message = f"""Please optimize my resume for ATS systems based on the following data:

## RESUME DATA:
{resume_json}

## JOB DESCRIPTION:
{job_description}

Please format the optimized resume in HTML format that I can directly use.
"""
    return user_message


def _parse_llm_response(content: str) -> str:
    content = content.replace("```html", "").replace("```", "")
    return content
