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
