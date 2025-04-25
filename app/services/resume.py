from typing import Any, Dict, List

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

    return db_resume_to_dict(resume)


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

    # Add personal info
    personal_info = PersonalInfo(
        resume=resume,
        name=data.get("personal_info", {}).get("name", ""),
        location=data.get("personal_info", {}).get("location", ""),
        email=data.get("personal_info", {}).get("email", ""),
        linkedin=data.get("personal_info", {}).get("linkedin", ""),
        github=data.get("personal_info", {}).get("github", ""),
    )
    session.add(personal_info)

    # Add skills
    skills = SkillSet(
        resume=resume,
        programming_languages=data.get("skills", {}).get("programming_languages", ""),
        frameworks=data.get("skills", {}).get("frameworks", ""),
        developer_tools=data.get("skills", {}).get("developer_tools", ""),
    )
    session.add(skills)

    # Add experiences
    for exp_data in data.get("experience", []):
        experience = Experience(
            resume=resume,
            title=exp_data.get("title", ""),
            company=exp_data.get("company", ""),
            location=exp_data.get("location", ""),
            start_date=exp_data.get("start_date", ""),
            end_date=exp_data.get("end_date", ""),
            points=exp_data.get("points", ""),
        )
        session.add(experience)

    # Add projects
    for proj_data in data.get("projects", []):
        project = Project(
            resume=resume,
            name=proj_data.get("name", ""),
            url=proj_data.get("url", ""),
            technologies=proj_data.get("technologies", ""),
            points=proj_data.get("points", []),
        )
        session.add(project)

    # Add education
    for edu_data in data.get("education", []):
        education = Education(
            resume=resume,
            institution=edu_data.get("institution", ""),
            degree=edu_data.get("degree", ""),
            graduation_date=edu_data.get("graduation_date", ""),
        )
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


async def update_entity_point(
    session: Session,
    entity_class,
    filter_by: Dict[str, Any],
    point_index: int,
    value: str,
) -> bool:
    """
    Update a point in an entity's points array (JSON field).
    Returns True on success. Raises NoResultFound if the entity was not found or index is out of range.
    """
    filter_conditions = []
    for key, val in filter_by.items():
        filter_conditions.append(getattr(entity_class, key) == val)
    entity = session.query(entity_class).filter(*filter_conditions).first()

    if not entity:
        raise NoResultFound(f"{entity_class.__name__} item not found for update.")
    try:
        points = entity.points
        if point_index >= len(points):
            raise NoResultFound(f"{entity_class.__name__} item not found for update.")
        points[point_index] = value
        entity.points = points
        session.commit()
        return True
    except AttributeError:
        raise ValueError(f"{entity_class.__name__} doesn't have points attribute")


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


async def update_project_point(
    session: Session, resume_id: int, project_id: int, point_index: int, value: str
) -> bool:
    """Update a specific project point"""
    return await update_entity_point(
        session, Project, {"id": project_id, "resume_id": resume_id}, point_index, value
    )


async def _add_item_to_collection(session: Session, resume_id: int, item_class, default_values=None):
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
            "points": [],
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
        "points": "• List key responsibilities and achievements here.",
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


async def delete_resume_by_id(session: Session, resume_id: int) -> bool:
    """Delete a resume by ID."""
    resume = await get_resume_by_id(session, resume_id)
    if not resume:
        raise NoResultFound(f"Resume with ID {resume_id} not found.")

    # Don't delete if it's the only resume
    count = session.query(Resume).count()
    if count <= 1:
        raise ValueError("Cannot delete the only resume. At least one resume must exist.")

    session.delete(resume)
    session.commit()
    return True
