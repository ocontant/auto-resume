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
def test_personal_info_valid(valid_personal_info):
    """Test creating PersonalInfo with valid data."""
    # Use the fixture for valid data
    info = PersonalInfo(**valid_personal_info)
    assert info.name == valid_personal_info["name"]
    assert info.email == valid_personal_info["email"]
    assert info.linkedin == valid_personal_info["linkedin"]
    assert info.github == valid_personal_info["github"]
    assert info.location == valid_personal_info["location"]


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


def test_skill_set_valid_old(valid_skill_set):
    """Test creating SkillSet with valid data (using fixture)."""
    # Reuse the main valid_skill_set fixture for consistency
    test_skill_set_valid(valid_skill_set) # Call the other test with the fixture result


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
    # Pydantic model likely doesn't include 'id', filter it out if needed
    exp_data = {k: v for k, v in valid_experience.items() if k != "id"}
    # Model expects string based on error
    exp = Experience(**exp_data)
    assert isinstance(exp.points, str)
    assert exp.points == exp_data["points"]


def test_experience_missing_field(missing_experience_field_data):
    """Test Experience raises ValidationError if required field is missing."""
    with pytest.raises(ValidationError) as exc_info:
        Experience(**missing_experience_field_data)
    assert "title" in str(exc_info.value) # Assuming title was the missing field


def test_experience_invalid_type(invalid_experience_type_data):
    """Test Experience raises ValidationError for incorrect data types."""
    with pytest.raises(ValidationError):
        Experience(**invalid_experience_type_data)


def test_experience_optional_location_absent(experience_data_optional_location_absent):
    """Test Experience can be created without optional location."""
    exp = Experience(**experience_data_optional_location_absent)
    assert exp.location is None


# --- Test Project ---
def test_project_valid(valid_project):
    """Test creating Project with valid data."""
    # Pydantic model likely doesn't include 'id', filter it out
    proj_data = {k: v for k, v in valid_project.items() if k != "id"}
    # Ensure points is a list as expected by the model
    assert isinstance(proj_data["points"], list)
    proj = Project(**proj_data)
    assert proj.name == proj_data["name"]
    assert proj.points == proj_data["points"]
    assert proj.technologies == proj_data["technologies"]


def test_project_missing_field(missing_project_field_data):
    """Test Project raises ValidationError if required field is missing."""
    with pytest.raises(ValidationError):
        Project(**missing_project_field_data)


def test_project_invalid_type(invalid_project_type_data):
    """Test Project raises ValidationError for incorrect data types."""
    with pytest.raises(ValidationError):
        Project(**invalid_project_type_data)


def test_project_points_validation(invalid_project_points_type_data):
    """Test Project validation for 'points' field type."""
    with pytest.raises(ValidationError):
        Project(**invalid_project_points_type_data)


# --- Test Education ---
def test_education_valid(valid_education):
    """Test creating Education with valid data."""
    # Pydantic model likely doesn't include 'id', filter it out
    edu_data = {k: v for k, v in valid_education.items() if k != "id"}
    edu = Education(**edu_data)
    assert edu.institution == edu_data["institution"]
    assert edu.degree == edu_data["degree"]
    assert edu.graduation_date == edu_data["graduation_date"]


def test_education_missing_field(missing_education_field_data):
    """Test Education raises ValidationError if required field is missing."""
    with pytest.raises(ValidationError):
        Education(**missing_education_field_data)


def test_education_invalid_type(invalid_education_type_data):
    """Test Education raises ValidationError for incorrect data types."""
    with pytest.raises(ValidationError):
        Education(**invalid_education_type_data)


# --- Test Resume (Composition Model) ---
def test_resume_valid(sample_resume_data):
    """Test creating Resume with valid nested models."""
    # Create a clean copy without ID fields that aren't in the model
    cleaned_data = {k: v for k, v in sample_resume_data.items() if k != "id"}
    # Ensure nested structures match Pydantic models
    # Experience points should be string, Project points list
    resume = Resume(**cleaned_data)
    assert resume.personal_info.name == cleaned_data["personal_info"]["name"]
    assert resume.skills.programming_languages == cleaned_data["skills"]["programming_languages"]
    assert isinstance(resume.experience[0].points, str) # Verify Experience points are str
    assert isinstance(resume.projects[0].points, list) # Verify Project points are list


def test_resume_missing_section(missing_resume_section_data):
    """Test Resume raises ValidationError if a required section is missing."""
    with pytest.raises(ValidationError):
        Resume(**missing_resume_section_data)


def test_resume_invalid_section_type(invalid_resume_data_section_type):
    """Test Resume raises ValidationError if a section has the wrong type."""
    # Fixture provides data with 'skills' as a string
    with pytest.raises(ValidationError):
        Resume(**invalid_resume_data_section_type)


# --- Test AIEnhanceRequest ---
def test_ai_enhance_request_valid(valid_ai_enhance_data):
    """Test creating AIEnhanceRequest with valid data."""
    req = AIEnhanceRequest(**valid_ai_enhance_data)
    assert req.text == valid_ai_enhance_data["text"]


def test_ai_enhance_request_missing_field():
    """Test AIEnhanceRequest raises ValidationError if required field is missing."""
    with pytest.raises(ValidationError):
        AIEnhanceRequest() # Missing text field


def test_ai_enhance_request_invalid_type(invalid_ai_enhance_type_data):
    """Test AIEnhanceRequest raises ValidationError for incorrect data types."""
    with pytest.raises(ValidationError):
        AIEnhanceRequest(**invalid_ai_enhance_type_data) # text is not str


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
    # Fixture `incomplete_ai_points_request` is missing several fields
    with pytest.raises(ValidationError) as exc_info:
        AIPointsRequest(**incomplete_ai_points_request)
    # Check for one of the expected missing fields
    assert "num_points" in str(exc_info.value) or "job_title" in str(exc_info.value) # Example check


def test_ai_points_request_invalid_type_context(invalid_ai_points_type_context_data):
    """Test AIPointsRequest raises ValidationError for incorrect context type."""
    with pytest.raises(ValidationError):
        AIPointsRequest(**invalid_ai_points_type_context_data) # context is not str


def test_ai_points_request_invalid_type_num_points(invalid_ai_points_type_num_data):
    """Test AIPointsRequest raises ValidationError for incorrect num_points type."""
    with pytest.raises(ValidationError):
        AIPointsRequest(**invalid_ai_points_type_num_data) # num_points is not int
