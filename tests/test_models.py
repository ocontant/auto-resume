"""Test suite for Pydantic models (app.models)."""

# Import your models here

# Note: Fixtures for valid data instances might be useful, defined in conftest.py


# --- Test PersonalInfo ---
def test_personal_info_valid():
    """Test creating PersonalInfo with valid data."""


def test_personal_info_missing_field():
    """Test PersonalInfo raises ValidationError if required field is missing."""


def test_personal_info_invalid_type():
    """Test PersonalInfo raises ValidationError for incorrect data types."""


# --- Test SkillSet ---
def test_skill_set_valid():
    """Test creating SkillSet with valid data."""


def test_skill_set_missing_field():
    """Test SkillSet raises ValidationError if required field is missing."""


def test_skill_set_invalid_type():
    """Test SkillSet raises ValidationError for incorrect data types."""


# --- Test Experience ---
def test_experience_valid():
    """Test creating Experience with valid data."""


def test_experience_missing_field():
    """Test Experience raises ValidationError if required field is missing."""


def test_experience_invalid_type():
    """Test Experience raises ValidationError for incorrect data types."""


def test_experience_optional_location_present():
    """Test Experience can be created with optional location."""


def test_experience_optional_location_absent():
    """Test Experience can be created without optional location."""


# --- Test Project ---
def test_project_valid():
    """Test creating Project with valid data."""


def test_project_missing_field():
    """Test Project raises ValidationError if required field is missing."""


def test_project_invalid_type():
    """Test Project raises ValidationError for incorrect data types."""


def test_project_points_list_of_strings():
    """Test Project validation for 'points' field (list of strings)."""


def test_project_points_invalid_type_in_list():
    """Test Project raises ValidationError if 'points' contains non-strings."""


def test_project_points_not_a_list():
    """Test Project raises ValidationError if 'points' is not a list."""


# --- Test Education ---
def test_education_valid():
    """Test creating Education with valid data."""


def test_education_missing_field():
    """Test Education raises ValidationError if required field is missing."""


def test_education_invalid_type():
    """Test Education raises ValidationError for incorrect data types."""


# --- Test Resume (Composition Model) ---
def test_resume_valid(
    valid_personal_info,
    valid_skill_set,
    valid_experience_list,
    valid_project_list,
    valid_education_list,
):
    """Test creating Resume with valid nested models."""


def test_resume_missing_section():
    """Test Resume raises ValidationError if a required section is missing."""


def test_resume_invalid_section_type():
    """Test Resume raises ValidationError if a section has the wrong type."""


# --- Test AIEnhanceRequest ---
def test_ai_enhance_request_valid():
    """Test creating AIEnhanceRequest with valid data."""


def test_ai_enhance_request_missing_field():
    """Test AIEnhanceRequest raises ValidationError if required field is missing."""


def test_ai_enhance_request_invalid_type():
    """Test AIEnhanceRequest raises ValidationError for incorrect data types."""


# --- Test AIPointsRequest ---
def test_ai_points_request_valid():
    """Test creating AIPointsRequest with valid data."""


def test_ai_points_request_missing_field():
    """Test AIPointsRequest raises ValidationError if required field is missing."""


def test_ai_points_request_invalid_type():
    """Test AIPointsRequest raises ValidationError for incorrect data types."""
