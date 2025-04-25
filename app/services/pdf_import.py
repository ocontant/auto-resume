import fitz # noqa
from sqlalchemy.orm import Session
from typing import Dict, Any

from litellm import completion
from app.services.resume import create_resume
from app.db import Resume


async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        with fitz.open(stream=file_content, filetype="pdf") as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
            return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


async def parse_resume_text(text: str) -> Dict[str, Any]:
    """Use LiteLLM to parse resume text into structured data matching our models."""
    prompt = f"""
    Extract the following information from this resume text and format it as a JSON object:
    
    Resume Text:
    {text}
    
    Extract the following sections:
    1. Personal Information (name, email, location, linkedin, github)
    2. Skills (programming_languages, frameworks, developer_tools)
    3. Work Experience (list of jobs with title, company, location, start_date, end_date, points/description)
    4. Projects (name, url, technologies, points/description)
    5. Education (institution, degree, graduation_date)
    
    Format the response as valid JSON matching this structure:
    {{
        "personal_info": {{
            "name": "...",
            "location": "...",
            "email": "...",
            "linkedin": "...",
            "github": "..."
        }},
        "skills": {{
            "programming_languages": "...",
            "frameworks": "...",
            "developer_tools": "..."
        }},
        "experience": [
            {{
                "title": "...",
                "company": "...",
                "location": "...",
                "start_date": "...",
                "end_date": "...",
                "points": "..."
            }}
        ],
        "projects": [
            {{
                "name": "...",
                "url": "...",
                "technologies": "...",
                "points": []
            }}
        ],
        "education": [
            {{
                "institution": "...",
                "degree": "...",
                "graduation_date": "..."
            }}
        ]
    }}
    
    If you can't find specific information, use empty strings or appropriate default values.
    Only return the JSON object, no additional text.
    """
    
    try:
        response = completion(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a resume parsing assistant that extracts structured data from resume text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        
        content = response.choices[0].message.content
        
        # Find JSON in the response
        import json
        import re
        
        # Try to extract JSON from the response if it's wrapped in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if json_match:
            content = json_match.group(1)
        
        # Parse the JSON response
        resume_data = json.loads(content)
        return resume_data
    
    except Exception as e:
        raise ValueError(f"Error parsing resume text: {str(e)}")


async def import_resume_from_pdf(file_content: bytes, session: Session, name: str = "Imported Resume") -> Resume:
    """Process a PDF resume file and create a new resume in the database."""
    text = await extract_text_from_pdf(file_content)
    parsed_data = await parse_resume_text(text)
    
    resume = await create_resume(session, name, parsed_data)
    return resume
