from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import AIEnhanceRequest, AIPointsRequest
from app.utils.ai import enhance_resume_text, generate_experience_points

router = APIRouter(prefix="/api/ai")


@router.post("/enhance", response_class=JSONResponse)
async def enhance_with_ai(request: AIEnhanceRequest):
    """Enhance text with AI to make it more impactful and professional."""
    try:
        enhanced_text = await enhance_resume_text(request.text)
        return {"enhanced_text": enhanced_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI enhancement failed: {str(e)}")


@router.post("/generate-points", response_class=JSONResponse)
async def generate_points(request: AIPointsRequest):
    """Generate bullet points for a job position based on title and company."""
    try:
        points = await generate_experience_points(request.job_title, request.company)
        return {"points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI point generation failed: {str(e)}")