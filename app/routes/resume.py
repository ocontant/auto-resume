from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Dict, Any

from app.models import Experience, Resume
import app.main as main

router = APIRouter(prefix="/api/resume")
templates = Jinja2Templates(directory="app/templates")


# Get complete resume
@router.get("/", response_class=JSONResponse)
async def get_resume():
    return main.current_resume


# Update complete resume
@router.post("/", response_class=JSONResponse)
async def update_resume(resume: Dict[str, Any]):
    main.current_resume = resume
    return {"success": True}


# Add new experience
@router.post("/experience", response_class=HTMLResponse)
async def add_experience(request: Request):
    new_exp = {
        "title": "New Position",
        "company": "Company Name",
        "location": "Location",
        "start_date": "Start Date",
        "end_date": "Present",
        "points": ["Describe your responsibilities and achievements..."]
    }

    main.current_resume["experience"].append(new_exp)
    index = len(main.current_resume["experience"]) - 1

    return templates.TemplateResponse(
        "components/experience_item.html",
        {"request": request, "item": new_exp, "index": index}
    ) 
 
 
# Delete experience
@router.delete("/experience/{index}", response_class=JSONResponse)
async def delete_experience(index: int):
    if 0 <= index < len(main.current_resume["experience"]):
        main.current_resume["experience"].pop(index) 
        return {"success": True}
    return {"success": False, "error": "Invalid index"}
 
 
# Update experience field
@router.patch("/experience/{index}/{field}", response_class=HTMLResponse)
async def update_experience_field(index: int, field: str, request: Request):
    form = await request.form()
    value = form.get("value", "")
    
    if 0 <= index < len(main.current_resume["experience"]):
        if field in main.current_resume["experience"][index]:
            main.current_resume["experience"][index][field] = value
            return f"{value}" # Return just the value as HTML for HTMX to swap
    return "Error updating field"
 
# Update experience point
@router.patch("/experience/{exp_index}/point/{point_index}", response_class=HTMLResponse)
async def update_experience_point(exp_index: int, point_index: int, request: Request):
    form = await request.form()
    value = form.get("value", "")
    
    if (0 <= exp_index < len(main.current_resume["experience"]) and
            0 <= point_index < len(main.current_resume["experience"][exp_index]["points"])):
        main.current_resume["experience"][exp_index]["points"][point_index] = value
        return f"{value}" # Return just the value as HTML for HTMX to swap
    return "Error updating point"


# Add point to experience
@router.post("/experience/{index}/point", response_class=HTMLResponse)
async def add_experience_point(index: int, request: Request):
    if 0 <= index < len(main.current_resume["experience"]):
        main.current_resume["experience"][index]["points"].append("New responsibility or achievement...")
        point_index = len(main.current_resume["experience"][index]["points"]) - 1

        return templates.TemplateResponse(
            "components/point_item.html",
            {
                "request": request,
                "point": "New responsibility or achievement...",
                "exp_index": index,
                "point_index": point_index
            }
        )
    raise HTTPException(status_code=404, detail="Experience not found")


# Delete point from experience
@router.delete("/experience/{exp_index}/point/{point_index}", response_class=JSONResponse)
async def delete_experience_point(exp_index: int, point_index: int):
    if (0 <= exp_index < len(main.current_resume["experience"]) and
            0 <= point_index < len(main.current_resume["experience"][exp_index]["points"])):
        main.current_resume["experience"][exp_index]["points"].pop(point_index)
        return {"success": True}
    return {"success": False, "error": "Invalid indices"}