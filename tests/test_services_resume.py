"""Test suite for Resume service functions (app.services.resume)."""

import pytest

# Note: Fixtures like mock_session, default_resume, sample_education, etc.
# would be defined in tests/conftest.py


# --- Test get_resume_by_id ---
@pytest.mark.asyncio
async def test_get_resume_by_id_found(mock_session):
    """Test retrieving an existing resume by its ID."""


@pytest.mark.asyncio
async def test_get_resume_by_id_not_found(mock_session):
    """Test retrieving a non-existent resume by ID returns None."""


# --- Test get_or_create_default_resume ---
@pytest.mark.asyncio
async def test_get_or_create_default_resume_creates_new(mock_session):
    """Test that a new default resume is created when none exists."""


@pytest.mark.asyncio
async def test_get_or_create_default_resume_returns_existing(mock_session, existing_resume_data):
    """Test that the existing resume is returned if one exists."""


# --- Test _resume_to_dict ---
def test_resume_to_dict_conversion(sample_resume_object):
    """Test conversion of a SQLAlchemy Resume object to a dictionary."""


def test_resume_to_dict_handles_missing_optional_relations(
    sample_resume_object_missing_data,  # Use the configured mock fixture
):
    """Test dictionary conversion handles missing optional relations."""


# --- Test update_personal_info ---
@pytest.mark.asyncio
async def test_update_personal_info_success(mock_session, default_resume):
    """Test successfully updating a field in PersonalInfo."""


@pytest.mark.asyncio
async def test_update_personal_info_not_found(mock_session):
    """Test updating PersonalInfo raises NoResultFound if resume doesn't exist."""


@pytest.mark.asyncio
async def test_update_personal_info_invalid_field(mock_session, default_resume):
    """Test updating PersonalInfo raises ValueError for an invalid field."""


# --- Test update_skills ---
@pytest.mark.asyncio
async def test_update_skills_success(mock_session, default_resume):
    """Test successfully updating a field in SkillSet."""


@pytest.mark.asyncio
async def test_update_skills_not_found(mock_session):
    """Test updating SkillSet raises NoResultFound if resume doesn't exist."""


@pytest.mark.asyncio
async def test_update_skills_invalid_field(mock_session, default_resume):
    """Test updating SkillSet raises ValueError for an invalid field."""


# --- Test update_education_field ---
@pytest.mark.asyncio
async def test_update_education_field_success(mock_session, sample_education_object):
    """Test successfully updating a field in an Education entry."""


@pytest.mark.asyncio
async def test_update_education_field_not_found(mock_session):
    """Test updating Education raises NoResultFound if entry doesn't exist."""


@pytest.mark.asyncio
async def test_update_education_field_invalid_field(mock_session, sample_education_object):
    """Test updating Education raises ValueError for an invalid field."""


# --- Test update_experience_field ---
@pytest.mark.asyncio
async def test_update_experience_field_success(mock_session, sample_experience_object):
    """Test successfully updating a field in an Experience entry."""


@pytest.mark.asyncio
async def test_update_experience_field_not_found(mock_session):
    """Test updating Experience raises NoResultFound if entry doesn't exist."""


@pytest.mark.asyncio
async def test_update_experience_field_invalid_field(mock_session, sample_experience_object):
    """Test updating Experience raises ValueError for an invalid field."""


# --- Test update_project_field ---
@pytest.mark.asyncio
async def test_update_project_field_success(mock_session, sample_project_object):
    """Test successfully updating a field in a Project entry."""


@pytest.mark.asyncio
async def test_update_project_field_not_found(mock_session, default_resume):
    """Test updating Project raises NoResultFound if entry doesn't exist."""


@pytest.mark.asyncio
async def test_update_project_field_invalid_field(mock_session, sample_project_object):
    """Test updating Project raises ValueError for an invalid field."""


# --- Test update_project_point ---
@pytest.mark.asyncio
async def test_update_project_point_success(mock_session, sample_project_with_description):
    """Test successfully updating a point in a Project's points list."""


@pytest.mark.asyncio
async def test_update_project_point_project_not_found(mock_session, default_resume):
    """Test updating Project point raises NoResultFound if project doesn't exist."""


# --- Test add_education ---
@pytest.mark.asyncio
async def test_add_education_success(mock_session, default_resume):
    """Test successfully adding a new Education entry."""


# --- Test delete_education_by_id ---
@pytest.mark.asyncio
async def test_delete_education_by_id_success(mock_session, sample_education_object):
    """Test successfully deleting an Education entry by ID."""


@pytest.mark.asyncio
async def test_delete_education_by_id_not_found(mock_session):
    """Test deleting Education raises NoResultFound if entry doesn't exist."""


# --- Test add_project ---
@pytest.mark.asyncio
async def test_add_project_success(mock_session, default_resume):
    """Test successfully adding a new Project entry."""


# --- Test delete_project_by_id ---
@pytest.mark.asyncio
async def test_delete_project_by_id_success(mock_session, sample_project_object):
    """Test successfully deleting a Project entry by ID."""


@pytest.mark.asyncio
async def test_delete_project_by_id_not_found(mock_session):
    """Test deleting Project raises NoResultFound if entry doesn't exist."""


# --- Test add_experience ---
@pytest.mark.asyncio
async def test_add_experience_success(mock_session, default_resume):
    """Test successfully adding a new Experience entry."""


# --- Test delete_experience_by_id ---
@pytest.mark.asyncio
async def test_delete_experience_by_id_success(mock_session, sample_experience_object):
    """Test successfully deleting an Experience entry by ID."""


@pytest.mark.asyncio
async def test_delete_experience_by_id_not_found(mock_session):
    """Test deleting Experience raises NoResultFound if entry doesn't exist."""
