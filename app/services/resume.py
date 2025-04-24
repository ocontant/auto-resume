from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from app.db import Resume, Education, Project, Experience, PersonalInfo, SkillSet


async def get_resume_by_id(session: Session, resume_id: int) -> Optional[Resume]:
    """Get a resume by ID"""
    return session.query(Resume).filter(Resume.id == resume_id).first()


async def get_or_create_default_resume(session: Session) -> Dict[str, Any]:
    """Get or create a default resume"""
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
        
        # Create a default experience entry
        experience = Experience(
            resume=resume,
            title="Sample Job Title",
            company="Sample Company",
            location="City, Country",
            start_date="Jan 2023",
            end_date="Present",
            points=["Responsibility or achievement 1.", "Responsibility or achievement 2."]
        )
        
        session.add(resume)
        session.add(personal_info)
        session.add(skills)
        session.add(experience) # Add the default experience to the session
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
            {"id": edu.id, "institution": edu.institution, "degree": edu.degree, "graduation_date": edu.graduation_date}
            for edu in resume.education
        ],
        "experience": [
            {"id": exp.id, "title": exp.title, "company": exp.company, "location": exp.location,
             "start_date": exp.start_date, "end_date": exp.end_date, "points": exp.points}
            for exp in resume.experience
        ],
        "projects": [
            {"id": proj.id, "name": proj.name, "url": proj.url, "technologies": proj.technologies, "points": proj.points}
            for proj in resume.projects
        ]
    }


async def update_entity_field(
    session: Session, 
    entity_class, 
    filter_by: Dict[str, Any], 
    field: str, 
    value: str
) -> bool:
    """
    Generic function to update any entity field
    """
    # Validate the field exists on the model
    if not hasattr(entity_class, field):
        raise ValueError(f"Invalid field: {field} for {entity_class.__name__}")
    
    # Build filter conditions
    filter_conditions = []
    for key, val in filter_by.items():
        filter_conditions.append(getattr(entity_class, key) == val)
    
    # Create and execute update statement
    stmt = update(entity_class).where(*filter_conditions).values({field: value})
    result = session.execute(stmt)
    session.commit()
    
    if result.rowcount == 0:
        raise NoResultFound(f"{entity_class.__name__} not found")
    
    return True


async def update_entity_point(
    session: Session, 
    entity_class, 
    filter_by: Dict[str, Any], 
    point_index: int, 
    value: str
) -> None:
    """
    Update a point in an entity's points array
    """
    filter_conditions = []
    for key, val in filter_by.items():
        filter_conditions.append(getattr(entity_class, key) == val)
    
    entity = session.query(entity_class).filter(*filter_conditions).first()
    
    if not entity:
        raise NoResultFound(f"{entity_class.__name__} not found with given criteria")
    
    try:
        points = entity.points
        if point_index >= len(points):
            raise IndexError(f"Point index {point_index} out of range")
        
        points[point_index] = value
        entity.points = points
        session.commit()
    except AttributeError:
        raise ValueError(f"{entity_class.__name__} doesn't have points attribute")


# Specialized functions for each entity type
async def update_personal_info(session: Session, resume_id: int, field: str, value: str) -> bool:
    """Update a personal info field"""
    return await update_entity_field(session, PersonalInfo, {"resume_id": resume_id}, field, value)


async def update_skills(session: Session, resume_id: int, field: str, value: str) -> bool:
    """Update a skills field"""
    return await update_entity_field(session, SkillSet, {"resume_id": resume_id}, field, value)


async def update_education_field(session: Session, education_id: int, field: str, value: str) -> None:
    """Update an education field"""
    await update_entity_field(session, Education, {"id": education_id}, field, value)


async def update_experience_field(session: Session, experience_id: int, field: str, value: str) -> None:
    """Update an experience field"""
    await update_entity_field(session, Experience, {"id": experience_id}, field, value)


async def update_experience_point(session: Session, experience_id: int, point_index: int, value: str) -> None:
    """Update a specific experience point"""
    await update_entity_point(session, Experience, {"id": experience_id}, point_index, value)


async def update_project_field(session: Session, resume_id: int, project_id: int, field: str, value: str) -> None:
    """Update a project field"""
    await update_entity_field(session, Project, {"id": project_id, "resume_id": resume_id}, field, value)


async def update_project_point(session: Session, resume_id: int, project_id: int, point_index: int, value: str) -> None:
    """Update a specific project point"""
    await update_entity_point(session, Project, {"id": project_id, "resume_id": resume_id}, point_index, value)


# Generic helper function for adding items to collections
async def _add_item_to_collection(session: Session, resume_id: int, item_class, default_values=None):
    """Generic function to add an item to a resume collection"""
    item = item_class(resume_id=resume_id, **(default_values or {}))
    session.add(item)
    session.commit()
    return item


# Specific implementation for education items
async def add_education(session: Session, resume_id: int) -> Education:
    """Add a new education entry to a resume"""
    return await _add_item_to_collection(session, resume_id, Education, {
        "institution": "University Name",
        "degree": "Degree/Program",
        "graduation_date": "Month Year"
    })


async def delete_education_by_id(session: Session, education_id: int) -> bool:
    """Delete an education entry by its ID."""
    education_entry = session.query(Education).filter(Education.id == education_id).first()
    if not education_entry:
        return False  # Or raise NoResultFound
    session.delete(education_entry)
    session.commit()
    return True


# Specific implementation for project items
async def add_project(session: Session, resume_id: int) -> Project:
    """Add a new project to a resume"""
    return await _add_item_to_collection(session, resume_id, Project, {
        "name": "Project Name",
        "url": "github.com/username/project",
        "technologies": "Technology 1, Technology 2",
        "points": []
    })


async def delete_project_by_id(session: Session, project_id: int) -> bool:
    """Delete a project by its ID."""
    project_entry = session.query(Project).filter(Project.id == project_id).first()
    if not project_entry:
        return False # Or raise NoResultFound
    session.delete(project_entry)
    session.commit()
    return True