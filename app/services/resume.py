from typing import Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db import Resume, Education, Project, Experience, PersonalInfo, SkillSet


async def get_resume_by_id(session: Session, resume_id: int) -> Optional[Resume]:
    """Get a resume by ID"""
    return session.query(Resume).filter(Resume.id == resume_id).first()


async def get_or_create_default_resume(session: Session) -> Dict[str, Any]:
    """Get or create a default resume"""
    # Check if we have any resume in the database
    resume = session.query(Resume).first()
    
    if not resume:
        # Create a new resume with default values
        resume = Resume(name="Default Resume")
        
        # Create personal info
        personal_info = PersonalInfo(
            resume=resume,
            name="Your Name",
            location="City, Country",
            email="your.email@example.com",
            linkedin="linkedin.com/in/yourprofile",
            github="github.com/yourusername"
        )
        
        # Create skills
        skills = SkillSet(
            resume=resume,
            programming_languages="Python, JavaScript, Java",
            frameworks="React, Django, FastAPI",
            developer_tools="Git, Docker, VS Code"
        )
        
        session.add(resume)
        session.add(personal_info)
        session.add(skills)
        session.commit()
    
    # Convert to dictionary for template rendering
    return _resume_to_dict(resume)


# Private helper function to convert database models to dict
def _resume_to_dict(resume: Resume) -> Dict[str, Any]:
    """Convert resume database object to dictionary for templates"""
    return {
        "id": resume.id,
        "name": resume.name,
        "personal_info": {
            "name": resume.personal_info.name if resume.personal_info else "",
            "location": resume.personal_info.location if resume.personal_info else "",
            "email": resume.personal_info.email if resume.personal_info else "",
            "linkedin": resume.personal_info.linkedin if resume.personal_info else "",
            "github": resume.personal_info.github if resume.personal_info else ""
        },
        "skills": {
            "programming_languages": resume.skills.programming_languages if resume.skills else "",
            "frameworks": resume.skills.frameworks if resume.skills else "",
            "developer_tools": resume.skills.developer_tools if resume.skills else ""
        },
        "education": [
            {"institution": edu.institution, "degree": edu.degree, "graduation_date": edu.graduation_date}
            for edu in resume.education
        ],
        "experience": [
            {"title": exp.title, "company": exp.company, "location": exp.location,
             "start_date": exp.start_date, "end_date": exp.end_date, "points": exp.points}
            for exp in resume.experience
        ],
        "projects": [
            {"name": proj.name, "url": proj.url, "technologies": proj.technologies, "points": proj.points}
            for proj in resume.projects
        ]
    }


# Generic helper function for adding items to collections
async def _add_item_to_collection(session: Session, resume_id: int, item_class, default_values=None):
    """Generic function to add an item to a resume collection"""
    resume = await get_resume_by_id(session, resume_id)
    if not resume:
        raise ValueError(f"Resume with ID {resume_id} not found")
    
    item = item_class(resume=resume, **(default_values or {}))
    session.add(item)
    session.commit()
    
    # Get the index based on the model type
    if item_class == Education:
        items = resume.education
    elif item_class == Project:
        items = resume.projects
    elif item_class == Experience:
        items = resume.experience
    
    return item, len(items) - 1


# Generic helper function for deleting items from collections
async def _delete_item_from_collection(session: Session, resume_id: int, index: int, get_items_func):
    """Generic function to delete an item from a resume collection"""
    resume = await get_resume_by_id(session, resume_id)
    if not resume:
        raise ValueError(f"Resume with ID {resume_id} not found")
    
    items = get_items_func(resume)
    if 0 <= index < len(items):
        session.delete(items[index])
        session.commit()


# Specific implementation for education items
async def add_education(session: Session, resume_id: int) -> Tuple[Education, int]:
    """Add a new education entry to a resume"""
    return await _add_item_to_collection(session, resume_id, Education, {
        "institution": "University Name",
        "degree": "Degree/Program",
        "graduation_date": "Month Year"
    })


async def delete_education(session: Session, resume_id: int, index: int) -> None:
    """Delete an education entry from a resume"""
    await _delete_item_from_collection(session, resume_id, index, lambda resume: resume.education)


# Specific implementation for project items
async def add_project(session: Session, resume_id: int) -> Tuple[Project, int]:
    """Add a new project to a resume"""
    return await _add_item_to_collection(session, resume_id, Project, {
        "name": "Project Name",
        "url": "github.com/username/project",
        "technologies": "Technology 1, Technology 2",
        "points": []
    })


async def delete_project(session: Session, resume_id: int, index: int) -> None:
    """Delete a project from a resume"""
    await _delete_item_from_collection(session, resume_id, index, lambda resume: resume.projects)