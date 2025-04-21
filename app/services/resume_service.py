from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import Resume, PersonalInfo, SkillSet, Experience


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
        
        # Initialize with an empty education list
        
        # Initialize with a sample work experience
        resume.experience = [
            Experience(
                title="Software Developer",
                company="Example Company",
                location="Remote",
                start_date="Jan 2020",
                end_date="Present",
                points=["Developed and maintained web applications using Python and JavaScript", 
                        "Implemented new features and improved application performance"]
            )
        ]

        # Initialize with sample projects
        from app.db import Project
        resume.projects = [
            Project(
                name="Resume Builder",
                url="github.com/yourusername/resume-builder",
                technologies="Python, FastAPI, SQLAlchemy, HTMX",
                points=["Created a web application for building professional resumes", 
                        "Implemented AI-assisted content generation for resume sections"]
            )
        ]
        
        session.add(resume)
        session.commit()
        session.refresh(resume)

    return resume