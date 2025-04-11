from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.models import AIEnhanceRequest, AIPointsRequest

router = APIRouter(prefix="/api/ai")


@router.post("/enhance", response_class=JSONResponse)
async def enhance_with_ai(request: AIEnhanceRequest):
    """Enhance text with AI to make it more impactful and professional."""
    # In a real implementation, this would call an AI service like OpenAI
    # For now, we'll simulate the AI enhancement

    original_text = request.text

    # Simple enhancement simulation
    enhanced_text = original_text

    # Add metrics if none exist
    if not any(x in original_text.lower() for x in ['%', 'percent', 'increased', 'decreased', 'improved']):
        enhanced_text += " resulting in 30% improvement in efficiency"

    # Make more action-oriented
    if not any(x in original_text.lower() for x in ['led', 'managed', 'developed', 'created', 'implemented']):
        enhanced_text = "Successfully implemented " + enhanced_text

    return {"enhanced_text": enhanced_text}


@router.post("/generate-points", response_class=JSONResponse)
async def generate_points(request: AIPointsRequest):
    """Generate bullet points for a job position based on title and company."""
    # In a real implementation, this would call an AI service

    job_title = request.job_title
    company = request.company

    # Sample generated points based on job title
    generated_points = []

    if "developer" in job_title.lower() or "engineer" in job_title.lower():
        generated_points = [
            f"Developed and maintained key features for {company}'s main product, resulting in 25% increase in user engagement",
            f"Collaborated with cross-functional teams to optimize application performance, reducing load times by 40%",
            f"Implemented automated testing processes, decreasing bug reports by 35% and improving code quality"
        ]
    elif "manager" in job_title.lower() or "lead" in job_title.lower():
        generated_points = [
            f"Led a team of 8 professionals at {company}, overseeing project delivery with 100% on-time completion rate",
            f"Implemented agile methodologies that increased team productivity by 30% and improved sprint planning accuracy",
            f"Managed stakeholder relationships and project budgets exceeding $500K, delivering all projects under budget"
        ]
    else:
        generated_points = [
            f"Contributed to {company}'s growth by implementing innovative solutions that increased operational efficiency by 20%",
            f"Collaborated with team members to improve existing processes, resulting in significant time and resource savings",
            f"Received recognition for exceptional performance and commitment to quality work"
        ]

    return {"points": generated_points}
