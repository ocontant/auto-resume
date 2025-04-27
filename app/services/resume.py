from typing import Any, Dict, List, Type

from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db import Education, Experience, PersonalInfo, Project, Resume, SkillSet
from app.models import db_resume_to_dict


async def get_resume_by_id(session: Session, resume_id: int) -> Resume:
    """Get a resume by ID"""
    resume = session.query(Resume).filter(Resume.id == resume_id).one_or_none()
    if not resume:
        raise NoResultFound(f"Resume with ID {resume_id} not found")
    return resume


async def get_resume_dict(session: Session, resume_id: int) -> Dict[str, Any]:
    """Get a resume by ID and convert it to a dictionary using Pydantic models"""
    resume = await get_resume_by_id(session, resume_id)
    if not resume:
        raise NoResultFound(f"Resume with ID {resume_id} not found")

    resume_dict = await db_resume_to_dict(resume)
    return resume_dict


async def get_all_resumes(session: Session) -> List[Dict[str, Any]]:
    """Get all resumes"""
    resumes = session.query(Resume).all()
    return [
        {
            "id": resume.id,
            "name": resume.name,
            "created_at": resume.created_at,
            "updated_at": resume.updated_at,
        }
        for resume in resumes
    ]


async def create_resume(session: Session, name: str, data: Dict[str, Any]) -> Resume:
    """Create a new resume with the provided data"""
    resume = Resume(name=name)
    session.add(resume)

    # Add personal info and skills
    personal_info = PersonalInfo(resume=resume, **data["personal_info"])
    session.add(personal_info)

    skills = SkillSet(resume=resume, **data["skills"])
    session.add(skills)

    # Add experiences
    for exp_data in data["experience"]:
        experience = Experience(resume=resume, **exp_data)
        session.add(experience)

    # Add projects
    for proj_data in data["projects"]:
        project = Project(resume=resume, **proj_data)
        session.add(project)

    # Add education
    for edu_data in data["education"]:
        education = Education(resume=resume, **edu_data)
        session.add(education)

    session.commit()
    session.refresh(resume)
    return resume


async def update_entity_field(
    session: Session, entity_class, filter_by: Dict[str, Any], field: str, value: str
) -> bool:
    """
    Generic function to update any entity field
    Returns True on success. Raises NoResultFound if the entity was not found.
    """
    if not hasattr(entity_class, field):
        raise ValueError(f"Invalid field: {field} for {entity_class.__name__}")
    filter_conditions = []
    for key, val in filter_by.items():
        filter_conditions.append(getattr(entity_class, key) == val)
    update_stmt = update(entity_class).where(*filter_conditions).values({field: value})
    result = session.execute(update_stmt)
    session.commit()
    if result.rowcount == 0:
        raise NoResultFound(f"{entity_class.__name__} not found with filter {filter_by}")
    return True


async def update_personal_info(session: Session, resume_id: int, field: str, value: str) -> bool:
    """Update a personal info field"""
    return await update_entity_field(session, PersonalInfo, {"resume_id": resume_id}, field, value)


async def update_skills(session: Session, resume_id: int, field: str, value: str) -> bool:
    """Update a skills field"""
    return await update_entity_field(session, SkillSet, {"resume_id": resume_id}, field, value)


async def update_education_field(
    session: Session, resume_id: int, education_id: int, field: str, value: str
) -> bool:
    """Update an education field"""
    education = (
        session.query(Education).filter(Education.id == education_id, Education.resume_id == resume_id).first()
    )
    if not education:
        raise NoResultFound(f"Education entry with ID {education_id} not found for resume {resume_id}.")
    return await update_entity_field(
        session, Education, {"id": education_id, "resume_id": resume_id}, field, value
    )


async def update_experience_field(
    session: Session, resume_id: int, experience_id: int, field: str, value: str
) -> bool:
    """Update an experience field"""
    experience = (
        session.query(Experience).filter(Experience.id == experience_id, Experience.resume_id == resume_id).first()
    )
    if not experience:
        raise NoResultFound(f"Experience entry with ID {experience_id} not found for resume {resume_id}.")
    return await update_entity_field(
        session, Experience, {"id": experience_id, "resume_id": resume_id}, field, value
    )


async def update_project_field(session: Session, resume_id: int, project_id: int, field: str, value: str) -> bool:
    """Update a project field"""
    return await update_entity_field(session, Project, {"id": project_id, "resume_id": resume_id}, field, value)


async def _add_item_to_collection(session: Session, resume_id: int, item_class: Type[Any], default_values=None):
    """Generic function to add an item to a resume collection"""
    item = item_class(resume_id=resume_id, **(default_values or {}))
    session.add(item)
    session.commit()
    return item


async def add_education(session: Session, resume_id: int) -> Education:
    """Add a new education entry to a resume"""
    return await _add_item_to_collection(
        session,
        resume_id,
        Education,
        {
            "institution": "University Name",
            "degree": "Degree/Program",
            "graduation_date": "Month Year",
        },
    )


async def delete_education_by_id(session: Session, resume_id: int, education_id: int) -> bool:
    """Delete an education entry by its ID."""
    education_entry = (
        session.query(Education).filter(Education.id == education_id, Education.resume_id == resume_id).first()
    )
    if not education_entry:
        raise NoResultFound(f"Education entry with ID {education_id} not found for resume {resume_id}.")
    session.delete(education_entry)
    session.commit()
    return True


async def add_project(session: Session, resume_id: int) -> Project:
    """Add a new project to a resume"""
    return await _add_item_to_collection(
        session,
        resume_id,
        Project,
        {
            "name": "Project Name",
            "url": "github.com/username/project",
            "technologies": "Technology 1, Technology 2",
            "description": "• Describe key features or details here.",
        },
    )


async def delete_project_by_id(session: Session, resume_id: int, project_id: int) -> bool:
    """Delete a project by its ID."""
    project_entry = session.query(Project).filter(Project.id == project_id, Project.resume_id == resume_id).first()
    if not project_entry:
        raise NoResultFound(f"Project entry with ID {project_id} not found for resume {resume_id}.")
    session.delete(project_entry)
    session.commit()
    return True


async def add_experience(session: Session, resume_id: int) -> Experience:
    """Add a new experience entry to a resume"""
    default_values = {
        "title": "New Job Title",
        "company": "Company Name",
        "location": "City, Country",
        "start_date": "Month Year",
        "end_date": "Present",
        "description": "• List key responsibilities and achievements here.",
    }
    return await _add_item_to_collection(session, resume_id, Experience, default_values)


async def delete_experience_by_id(session: Session, resume_id: int, experience_id: int) -> bool:
    """Delete an experience entry by its ID."""
    experience_entry = (
        session.query(Experience).filter(Experience.id == experience_id, Experience.resume_id == resume_id).first()
    )
    if not experience_entry:
        raise NoResultFound(f"Experience entry with ID {experience_id} not found for resume {resume_id}.")
    session.delete(experience_entry)
    session.commit()
    return True


async def delete_resume_by_id(session: Session, resume_id: int) -> None:
    """Delete a resume by ID."""
    resume = await get_resume_by_id(session, resume_id)
    if not resume:
        raise NoResultFound(f"Resume with ID {resume_id} not found.")

    session.delete(resume)
    session.commit()