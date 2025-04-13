from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Dict, Any

from app.models import Experience, Resume
import app.main as main
from app.utils.db import get_resume_section, get_full_resume, save_resume_section, init_db

router = APIRouter(prefix="/api/resume")
templates = Jinja2Templates(directory="app/templates")

# Initialize database on startup
init_db()

# Section endpoints
@router.get("/section/{section}", response_class=HTMLResponse)
async def get_section(request: Request, section: str):
    """Get a specific section of the resume form."""
    
    # Get data from database or use current_resume as fallback
    db_data = get_resume_section(section)
    if db_data:
        section_data = db_data
    else:
        # If not in DB yet, get from current_resume and save to DB
        if section in main.current_resume:
            section_data = main.current_resume[section]
            save_resume_section(section, section_data)
        else:
            section_data = {}
    
    template_map = {
        "personal": "components/personal_form.html",
        "experience": "components/resume_form.html",  # Reusing existing component
        "education": "components/education_form.html",
        "skills": "components/skills_form.html",
        "projects": "components/projects_form.html",
        "layout": "components/layout_form.html"
    }
    
    if section not in template_map:
        return HTMLResponse(
            content=f"<div class='p-4 bg-red-100 text-red-800 rounded'>Unknown section: {section}</div>",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Get the appropriate template for this section
    template = template_map[section]
    
    try:
        return templates.TemplateResponse(
            template,
            {"request": request, "resume_data": main.current_resume, "section_data": section_data}
        )
    except Exception as e:
        # For non-existing templates, return a placeholder
        return HTMLResponse(
            content=f"<div class='p-4 bg-yellow-100 text-yellow-800 rounded'>Coming soon: {section} tab</div>"
        )

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

# Skills endpoints
@router.patch("/skills/{field}", response_class=HTMLResponse)
async def update_skills_field(field: str, request: Request):
    form = await request.form()
    value = form.get("value", "")
    
    if field in main.current_resume["skills"]:
        main.current_resume["skills"][field] = value
        
        # Save to database
        save_resume_section("skills", main.current_resume["skills"])
        
        return f"{value}"
    return "Error updating field"

# Education endpoints
@router.post("/education", response_class=HTMLResponse)
async def add_education(request: Request):
    new_edu = {
        "institution": "University Name",
        "degree": "Degree / Program",
        "graduation_date": "Graduation Year"
    }

    main.current_resume["education"].append(new_edu)
    index = len(main.current_resume["education"]) - 1
    
    # Save to database
    save_resume_section("education", main.current_resume["education"])

    return templates.TemplateResponse(
        "components/education_item.html",
        {"request": request, "edu": new_edu, "index": index}
    )

@router.delete("/education/{index}", response_class=JSONResponse)
async def delete_education(index: int):
    if 0 <= index < len(main.current_resume["education"]):
        main.current_resume["education"].pop(index)
        
        # Save to database
        save_resume_section("education", main.current_resume["education"])
        
        return {"success": True}
    return {"success": False, "error": "Invalid index"}

@router.patch("/education/{index}/{field}", response_class=HTMLResponse)
async def update_education_field(index: int, field: str, request: Request):
    form = await request.form()
    value = form.get("value", "")
    
    if 0 <= index < len(main.current_resume["education"]):
        if field in main.current_resume["education"][index]:
            main.current_resume["education"][index][field] = value
            
            # Save to database
            save_resume_section("education", main.current_resume["education"])
            
            return f"{value}"
    return "Error updating field"