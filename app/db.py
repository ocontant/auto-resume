import os
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Ensure database directory exists
os.makedirs("app/data", exist_ok=True)

# Database settings
SQLITE_FILE_NAME = "resume.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

# let's keep session sync for while
engine = create_engine(SQLITE_URL)

# Create base model
Base = declarative_base()


# Define models
class PersonalInfo(Base):
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    email = Column(String, nullable=False)
    linkedin = Column(String, nullable=False)
    github = Column(String, nullable=False)

    # Relationship
    resume = relationship("Resume", back_populates="personal_info")


class SkillSet(Base):
    __tablename__ = "skillset"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    programming_languages = Column(String, nullable=False, default="")
    frameworks = Column(String, nullable=False, default="")
    developer_tools = Column(String, nullable=False, default="")

    # Relationship
    resume = relationship("Resume", back_populates="skills")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    institution = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    graduation_date = Column(String, nullable=False)

    # Relationship
    resume = relationship("Resume", back_populates="education")


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    points = Column(String, nullable=False, default="")  # Store as a single text block

    # Relationship
    resume = relationship("Resume", back_populates="experience")


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    technologies = Column(String, nullable=False)
    points = Column(JSON, nullable=False)  # Store as JSON array

    # Relationship
    resume = relationship("Resume", back_populates="projects")


class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default="Default Resume")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    personal_info = relationship(
        "PersonalInfo",
        back_populates="resume",
        uselist=False,
        cascade="all, delete-orphan",
    )
    skills = relationship("SkillSet", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    experience = relationship("Experience", back_populates="resume", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="resume", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="resume", cascade="all, delete-orphan")


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=True)
    description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Database initialization
def create_db_and_tables():
    Base.metadata.create_all(engine)


# Session dependency
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
