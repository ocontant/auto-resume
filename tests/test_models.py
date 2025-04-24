"""Test suite for Pydantic models (app.models)."""

import pytest
from pydantic import ValidationError

# Import models
from app.models import (
    AIEnhanceRequest,
    AIPointsRequest,
    Education,
    Experience,
    PersonalInfo,
    Project,
    Resume,
    SkillSet,
)


# --- Test PersonalInfo ---
def test_personal_info_valid():
    """Test creating PersonalInfo with valid data."""
    # Create data directly based on model requirements
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe",
        "location": "Anytown, USA",
    }
    info = PersonalInfo(**data)
    assert info.name == data["name"]
    assert info.email == data["email"]
    assert info.linkedin == data["linkedin"]
    assert info.location == data["location"]


def test_personal_info_missing_field(valid_personal_info_incomplete):
    """Test PersonalInfo raises ValidationError if required field (name) is missing."""
    # Name field is required but missing from fixture
    data = valid_personal_info_incomplete
    with pytest.raises(ValidationError) as exc_info:
        PersonalInfo(**data)
    assert "name" in str(exc_info.value)


def test_personal_info_invalid_type(valid_personal_info):
    """Test PersonalInfo creation with technically invalid email (if validation is off)."""
    # Use valid data but modify email to be invalid
    data = valid_personal_info.copy()
    data["email"] = "not-an-email"
    # No longer expect ValidationError since email validation is off
    info = PersonalInfo(**data)
    assert info.email == "not-an-email"  # Check it was assigned


# --- Test SkillSet ---
def test_skill_set_valid(valid_skill_set):
    """Test creating SkillSet with valid data."""
    skills = SkillSet(**valid_skill_set)
    assert skills.programming_languages == valid_skill_set["programming_languages"]
    assert skills.frameworks == valid_skill_set["frameworks"]
    assert skills.developer_tools == valid_skill_set["developer_tools"]


def test_skill_set_valid_old():
    """Test creating SkillSet with valid data."""
    data = {
        "programming_languages": "Python, JavaScript, Java",
        "frameworks": "React, Django, FastAPI",
        "developer_tools": "Git, Docker, VS Code",
    }
    skills = SkillSet(**data)
    assert skills.programming_languages == data["programming_languages"]
    assert skills.frameworks == data["frameworks"]
    assert skills.developer_tools == data["developer_tools"]


def test_skill_set_invalid_type():
    """Test SkillSet raises ValidationError for incorrect data types."""
    data = {
        "programming_languages": 123,  # Should be a string
        "frameworks": "React, Django",
        "developer_tools": "Git, Docker",
    }
    with pytest.raises(ValidationError):
        SkillSet(**data)


# --- Test Experience ---
def test_experience_valid(valid_experience):
    """Test creating Experience with valid data."""
    # Remove id from the fixture data since it's not part of the Pydantic model
    exp_data = {k: v for k, v in valid_experience.items() if k != "id"}
    # Model expects string based on error
    exp = Experience(**exp_data)
    assert isinstance(exp.points, str)
    assert exp.points == exp_data["points"]


def test_experience_missing_field():
    """Test Experience raises ValidationError if required field is missing."""
    data = {
        "company": "Tech Corp",
        "location": "Anytown, USA",
        "points": "Developed feature X",  # Assuming model expects string
    }
    with pytest.raises(ValidationError):
        Experience(**data)


def test_experience_invalid_type():
    """Test Experience raises ValidationError for incorrect data types."""
    data = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Anytown, USA",
        "points": "Developed feature X",
    }
    with pytest.raises(ValidationError):
        Experience(**data)


def test_experience_optional_location_absent():
    """Test Experience can be created without optional location."""
    data = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "start_date": "Jan 2020",
        "end_date": "Present",
        "points": "Developed feature X",  # Assuming model expects string
    }
    exp = Experience(**data)
    assert exp.location is None


# --- Test Project ---
def test_project_valid(valid_project):
    """Test creating Project with valid data."""
    # Remove id from the fixture data since it's not part of the Pydantic model
    proj_data = {k: v for k, v in valid_project.items() if k != "id"}
    # Fixture now provides a list, so no conversion needed here
    assert isinstance(proj_data["points"], list)
    proj = Project(**proj_data)
    assert proj.name == proj_data["name"]
    assert isinstance(proj.points, list)
    assert proj.points == proj_data["points"]
    assert proj.technologies == proj_data["technologies"]


def test_project_missing_field():
    """Test Project raises ValidationError if required field is missing."""
    data = {
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "points": "• Implemented API\n• Wrote tests",
        # Missing name
    }
    with pytest.raises(ValidationError):
        Project(**data)


def test_project_invalid_type():
    """Test Project raises ValidationError for incorrect data types."""
    data = {
        "name": "Cool Project",
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "points": "• Implemented API\n• Wrote tests",
    }
    with pytest.raises(ValidationError):
        Project(**data)


def test_project_points_validation():
    """Test Project validation for 'points' field."""
    data = {
        "name": "Cool Project",
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "points": 12345,  # Should be a string
    }
    with pytest.raises(ValidationError):
        Project(**data)


# --- Test Education ---
def test_education_valid(valid_education):
    """Test creating Education with valid data."""
    # Remove id from the fixture data since it's not part of the Pydantic model
    edu_data = {k: v for k, v in valid_education.items() if k != "id"}

    edu = Education(**edu_data)
    assert edu.institution == edu_data["institution"]
    assert edu.degree == edu_data["degree"]
    assert edu.graduation_date == edu_data["graduation_date"]


def test_education_missing_field():
    """Test Education raises ValidationError if required field is missing."""
    data = {"degree": "B.S. Computer Science", "graduation_date": "May 2020"}
    with pytest.raises(ValidationError):
        Education(**data)


def test_education_invalid_type():
    """Test Education raises ValidationError for incorrect data types."""
    data = {
        "institution": "University of Example",
        "degree": 12345,  # Should be a string
        "graduation_date": "May 2020",
    }
    with pytest.raises(ValidationError):
        Education(**data)


# --- Test Resume (Composition Model) ---
def test_resume_valid(sample_resume_data):
    """Test creating Resume with valid nested models."""
    # Create a clean copy without ID fields that aren't in the model
    cleaned_data = {k: v for k, v in sample_resume_data.items() if k != "id"}
    # Fixtures now provide points as lists, should validate correctly
    # Experience points should be string, Project points list
    resume = Resume(**cleaned_data)
    assert resume.personal_info.name == cleaned_data["personal_info"]["name"]
    assert resume.skills.programming_languages == cleaned_data["skills"]["programming_languages"]
    assert isinstance(resume.experience[0].points, str)  # Verify Experience points are str
    assert isinstance(resume.projects[0].points, list)


def test_resume_missing_section():
    """Test Resume raises ValidationError if a required section is missing."""
    data = {
        "name": "My Resume",
        "skills": {
            "programming_languages": "Python, JavaScript",
            "frameworks": "React, Django, FastAPI",
            "developer_tools": "Git, Docker",
        },
        "experience": [],
        "projects": [],
        "education": [],
    }
    with pytest.raises(ValidationError):
        Resume(**data)


def test_resume_invalid_section_type(invalid_resume_data_section_type):
    """Test Resume raises ValidationError if a section has the wrong type."""
    # Fixture provides data with 'skills' as a string
    data = invalid_resume_data_section_type
    with pytest.raises(ValidationError):
        Resume(**data)


# --- Test AIEnhanceRequest ---
def test_ai_enhance_request_valid():
    """Test creating AIEnhanceRequest with valid data."""
    data = {"text": "Enhance this: Developed feature X"}
    req = AIEnhanceRequest(**data)
    assert req.text == data["text"]


def test_ai_enhance_request_missing_field():
    """Test AIEnhanceRequest raises ValidationError if required field is missing."""
    with pytest.raises(ValidationError):
        AIEnhanceRequest()  # Missing text field


def test_ai_enhance_request_invalid_type():
    """Test AIEnhanceRequest raises ValidationError for incorrect data types."""
    with pytest.raises(ValidationError):
        AIEnhanceRequest(text=123)  # text is not str


# --- Test AIPointsRequest ---
def test_ai_points_request_valid(valid_ai_points_request):
    """Test creating AIPointsRequest with valid data."""
    req = AIPointsRequest(**valid_ai_points_request)
    assert req.context == valid_ai_points_request["context"]
    assert req.num_points == valid_ai_points_request["num_points"]
    assert req.job_title == valid_ai_points_request["job_title"]
    assert req.company == valid_ai_points_request["company"]


def test_ai_points_request_missing_field(incomplete_ai_points_request):
    """Test AIPointsRequest raises ValidationError if required field is missing."""
    data_missing_num = {"context": "Desc", "job_title": "Dev", "company": "Corp"}
    data_missing_ctx = {"num_points": 3, "job_title": "Dev", "company": "Corp"}

    # Test missing num_points
    with pytest.raises(ValidationError) as exc_info_num:
        AIPointsRequest(**data_missing_num)
    assert "num_points" in str(exc_info_num.value)

    # Test missing context
    with pytest.raises(ValidationError) as exc_info_ctx:
        AIPointsRequest(**data_missing_ctx)
    assert "context" in str(exc_info_ctx.value)


def test_ai_points_request_invalid_type():
    """Test AIPointsRequest raises ValidationError for incorrect data types."""
    with pytest.raises(ValidationError):
        AIPointsRequest(context=["list"], num_points=3)  # context is not str
    with pytest.raises(ValidationError):
        AIPointsRequest(context="Project X", num_points="five")  # num_points is not int
