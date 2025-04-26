from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PersonalInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    location: str
    email: str
    linkedin: str
    github: str
    id: Optional[int] = None
    resume_id: Optional[int] = None


class SkillSet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    programming_languages: str
    frameworks: str
    developer_tools: str
    id: Optional[int] = None
    resume_id: Optional[int] = None


class Experience(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    company: str
    location: Optional[str] = None
    start_date: str
    end_date: str
    points: str
    id: Optional[int] = None
    resume_id: Optional[int] = None


class Project(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    url: str
    technologies: str
    points: List[str]
    id: Optional[int] = None
    resume_id: Optional[int] = None


class Education(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    institution: str
    degree: str
    graduation_date: str
    id: Optional[int] = None
    resume_id: Optional[int] = None


class Resume(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    personal_info: PersonalInfo
    skills: SkillSet
    experience: List[Experience]
    projects: List[Project]
    education: List[Education]
    id: Optional[int] = None
    name: Optional[str] = None


class AIEnhanceRequest(BaseModel):
    text: str


class AIPointsRequest(BaseModel):
    context: str
    num_points: int
    job_title: str
    company: str


async def db_resume_to_dict(db_resume):
    """Convert a SQLAlchemy Resume object to a dictionary using Pydantic validation"""
    pydantic_resume = Resume.model_validate(db_resume)
    return pydantic_resume.model_dump()
