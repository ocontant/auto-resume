from typing import List, Optional

from pydantic import BaseModel


class PersonalInfo(BaseModel):
    name: str
    location: str
    email: str
    linkedin: str
    github: str


class SkillSet(BaseModel):
    programming_languages: str
    frameworks: str
    developer_tools: str


class Experience(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    start_date: str
    end_date: str
    points: str


class Project(BaseModel):
    name: str
    url: str
    technologies: str
    points: List[str]


class Education(BaseModel):
    institution: str
    degree: str
    graduation_date: str


class Resume(BaseModel):
    personal_info: PersonalInfo
    skills: SkillSet
    experience: List[Experience]
    projects: List[Project]
    education: List[Education]


class AIEnhanceRequest(BaseModel):
    text: str


class AIPointsRequest(BaseModel):
    job_title: str
    company: str
