from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import Resume, PersonalInfo, SkillSet


def get_resume_by_id(session: Session, resume_id: int) -> Type[Resume] | None:
    """Get a resume by its ID"""
    return session.get(Resume, resume_id)


def get_or_create_default_resume(session: Session) -> Resume:
    """Get the default resume or create one if it doesn't exist"""
    resume = session.execute(select(Resume)).scalar()

    if not resume:
        resume = Resume(name="My Resume")
        
        resume.personal_info = PersonalInfo(
            name="Your Name", 
            location="Your Location", 
            email="your.email@example.com",
            linkedin="linkedin.com/in/yourprofile", 
            github="github.com/yourusername"
        )
        
        resume.skills = SkillSet(
            programming_languages="Python, JavaScript",
            frameworks="FastAPI, React",
            developer_tools="Git, Docker"
        )
        
        session.add(resume)
        session.commit()
        session.refresh(resume)

    return resume
