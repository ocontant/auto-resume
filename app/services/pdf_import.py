import fitz  # noqa
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from sqlalchemy.orm import Session

from app.models import Resume
from app.services.config import get_llm_settings
from app.services.resume import create_resume


async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        # I am almost sure it will detect file type other than pdfs .-.
        with fitz.open(stream=file_content) as file:
            text = ""
            for page in file:
                text += page.get_text()
            return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


async def parse_resume_text(session, text: str) -> Resume:
    """Use Llamaindex to parse resume text into structured data matching our models."""
    api_key, model_name = await get_llm_settings(session)

    llm = OpenAI(api_key=api_key, model=model_name, temperature=0.1)
    structured_llm = llm.as_structured_llm(output_cls=Resume)

    prompt = f"""
You are an expert resume parser. Extract structured information from this resume:

RESUME TEXT:
{text}

---

Format the information exactly according to the Resume schema. Guidelines:
- For experience entries, convert bullet points into a single string with line breaks for the "points" field
- For projects, summarize the project description or features into the 'technologies' or 'name' field if appropriate, or omit detailed points. The Project model no longer has a 'points' field.
- For skills, categorize them into "technical_skills", "soft_skills", and "tools" as appropriate. Combine related skills into comma-separated strings for each field.
- Ensure all required fields are populated
- If specific information like name, location, email, linkedin, github is missing,
 use placeholders like '[NAME]', '[LOCATION]', '[EMAIL]', '[LINKEDIN]', '[GITHUB]'.
"""

    input_msg = ChatMessage.from_str(prompt)
    output = await structured_llm.achat([input_msg])

    return output.raw


async def import_resume_from_pdf(file_content: bytes, session: Session, name: str = "Imported Resume") -> Resume:
    """Process a PDF resume file and create a new resume in the database."""
    text = await extract_text_from_pdf(file_content)
    parsed_resume = await parse_resume_text(session, text)
    resume = await create_resume(session, name, parsed_resume.model_dump())
    return resume
