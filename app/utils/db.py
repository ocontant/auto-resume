import json
import os
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ensure the database directory exists
os.makedirs('db', exist_ok=True)

# Database URL
DATABASE_URL = "sqlite:///resume.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

# Define Resume model
class ResumeSection(Base):
    __tablename__ = "resume"
    
    id = Column(Integer, primary_key=True)
    section = Column(String, nullable=False, unique=True)
    data = Column(Text, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the SQLAlchemy database with required tables."""
    Base.metadata.create_all(bind=engine)
