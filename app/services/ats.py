from typing import Dict, Any
import os
import json
import re
from litellm import completion
from dotenv import load_dotenv


load_dotenv()

llm_initialized = False
DEFAULT_MODEL = "gpt-4.1-mini"


def init_llm():
    """Initialize LiteLLM with API keys from environment variables"""
    global llm_initialized
    
    if os.getenv("OPENAI_API_KEY"):
        print("OpenAI API key found, LiteLLM initialized")
        llm_initialized = True
    elif os.getenv("ANTHROPIC_API_KEY"):
        print("Anthropic API key found, LiteLLM initialized")
        llm_initialized = True
    else:
        print("Warning: No API keys found for LLM providers")


async def optimize_resume(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    if not llm_initialized:
        print("No LLM initialized, returning original resume")
        return resume_data
    
    prompt = _create_ats_prompt(resume_data)
    
    try:
        response = completion(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert resume writer specializing in creating ATS-optimized resumes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        optimized_resume = _parse_llm_response(content, resume_data)
        return optimized_resume
        
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return resume_data


def _create_ats_prompt(resume_data: Dict[str, Any]) -> str:
    """Create a prompt for the LLM based on the resume data"""
    return f"""
I need you to optimize the following resume to score highly on Applicant Tracking Systems (ATS).
Make it concise, impactful, and ensure it contains relevant keywords for the industry.
Don't invent new information, but rephrase and reorganize the existing content for maximum ATS score.

Here's the resume data:

PERSONAL INFORMATION:
Name: {resume_data['personal_info']['name']}
Location: {resume_data['personal_info']['location']}

SKILLS:
Programming Languages: {resume_data['skills']['programming_languages']}
Frameworks/Libraries: {resume_data['skills']['frameworks']}
Developer Tools: {resume_data['skills']['developer_tools']}

EXPERIENCE:
{json.dumps(resume_data['experience'], indent=2)}

PROJECTS:
{json.dumps(resume_data['projects'], indent=2)}

EDUCATION:
{json.dumps(resume_data['education'], indent=2)}

Please rewrite this resume to be ATS-optimized, keeping the same basic structure but improving the language and organization.
Format the response as clean plain text that can be directly rendered in an HTML template.
OUTPUT HTML FORMATED. IT Will be added inside a container. You can use Tailwind for it. Compact spacing
Apply required css to keep html formated
The outer div spacing should keep a small padding only besides font sans
"""


def _parse_llm_response(content: str, original_resume: Dict[str, Any]) -> Dict[str, Any]:
    cleaned_content = re.sub(r'^```\s*(?:html|HTML)?\s*\n', '', content.strip())
    cleaned_content = re.sub(r'\n```\s*$', '', cleaned_content)
    
    optimized = dict(original_resume)
    optimized["ats_content"] = cleaned_content
    
    return optimized
