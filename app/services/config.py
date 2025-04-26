from typing import Optional

from sqlalchemy.orm import Session

from app.db import Config
from app.services.ats import get_default_ats_prompt

# Constants for config keys
JOB_DESCRIPTION_KEY = "job_description"
ATS_PROMPT_KEY = "ats_prompt"


async def get_config_value(session: Session, key: str, default: Optional[str]) ->  str:
    """Get a configuration value by key"""
    config_entry = session.query(Config).filter(Config.key == key).first()
    if config_entry:
        return str(config_entry.value)
    return default


async def set_config_value(session: Session, key: str, value: Optional[str], description: Optional[str] = None) -> None:
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
