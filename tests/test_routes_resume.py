"""Test suite for Resume API endpoints (app.routes.resume)."""

import pytest
from fastapi.testclient import TestClient

# Note: Fixtures like client, mock_get_or_create_resume, mock_update_personal_info etc.
# would be defined in tests/conftest.py


# --- Test Section Endpoints (GET /section/*) ---
@pytest.mark.asyncio
async def test_get_personal_section(client: TestClient, mock_get_or_create_resume):
    """Test GET /api/resume/section/personal returns 200 OK."""


@pytest.mark.asyncio
async def test_get_experience_section(client: TestClient, mock_get_or_create_resume):
    """Test GET /api/resume/section/experience returns 200 OK."""


@pytest.mark.asyncio
async def test_get_skills_section(client: TestClient, mock_get_or_create_resume):
    """Test GET /api/resume/section/skills returns 200 OK."""


@pytest.mark.asyncio
async def test_get_education_section(client: TestClient, mock_get_or_create_resume):
    """Test GET /api/resume/section/education returns 200 OK."""


@pytest.mark.asyncio
async def test_get_projects_section(client: TestClient, mock_get_or_create_resume):
    """Test GET /api/resume/section/projects returns 200 OK."""


# --- Test PATCH /api/resume/personal_info/{field} ---
@pytest.mark.asyncio
async def test_update_personal_info_field_success(client: TestClient, mock_update_personal_info):
    """Test PATCH personal_info field succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_update_personal_info_field_not_found(client: TestClient, mock_update_personal_info_not_found):
    """Test PATCH personal_info field returns 404 if not found."""


@pytest.mark.asyncio
async def test_update_personal_info_field_server_error(client: TestClient, mock_update_personal_info_error):
    """Test PATCH personal_info field returns 500 on service error."""


@pytest.mark.asyncio
async def test_update_personal_info_field_validation_error(client: TestClient):
    """Test PATCH personal_info field returns 422 on missing form data."""


# --- Test PATCH /api/resume/skills/{field} ---
@pytest.mark.asyncio
async def test_update_skills_field_success(client: TestClient, mock_update_skills):
    """Test PATCH skills field succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_update_skills_field_not_found(client: TestClient, mock_update_skills_not_found):
    """Test PATCH skills field returns 404 if not found."""


@pytest.mark.asyncio
async def test_update_skills_field_server_error(client: TestClient, mock_update_skills_error):
    """Test PATCH skills field returns 500 on service error."""


@pytest.mark.asyncio
async def test_update_skills_field_validation_error(client: TestClient):
    """Test PATCH skills field returns 422 on missing form data."""


# --- Test PATCH /api/resume/education/{id}/{field} ---
@pytest.mark.asyncio
async def test_update_education_field_endpoint_success(client: TestClient, mock_update_education_field):
    """Test PATCH education field succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_update_education_field_endpoint_not_found(
    client: TestClient, mock_update_education_field_not_found
):
    """Test PATCH education field returns 404 if not found."""


@pytest.mark.asyncio
async def test_update_education_field_endpoint_server_error(client: TestClient, mock_update_education_field_error):
    """Test PATCH education field returns 500 on service error."""


@pytest.mark.asyncio
async def test_update_education_field_endpoint_validation_error(client: TestClient):
    """Test PATCH education field returns 422 on missing form data."""


# --- Test PATCH /api/resume/experience/{id}/{field} ---
@pytest.mark.asyncio
async def test_update_experience_field_endpoint_success(client: TestClient, mock_update_experience_field):
    """Test PATCH experience field succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_update_experience_field_endpoint_not_found(
    client: TestClient, mock_update_experience_field_not_found
):
    """Test PATCH experience field returns 404 if not found."""


@pytest.mark.asyncio
async def test_update_experience_field_endpoint_server_error(
    client: TestClient, mock_update_experience_field_error
):
    """Test PATCH experience field returns 500 on service error."""


@pytest.mark.asyncio
async def test_update_experience_field_endpoint_validation_error(client: TestClient):
    """Test PATCH experience field returns 422 on missing form data."""


# --- Test PATCH /api/resume/project/{id}/{field} ---
@pytest.mark.asyncio
async def test_update_project_field_endpoint_success(client: TestClient, mock_update_project_field):
    """Test PATCH project field succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_update_project_field_endpoint_not_found(client: TestClient, mock_update_project_field_not_found):
    """Test PATCH project field returns 404 if not found."""


@pytest.mark.asyncio
async def test_update_project_field_endpoint_server_error(client: TestClient, mock_update_project_field_error):
    """Test PATCH project field returns 500 on service error."""


@pytest.mark.asyncio
async def test_update_project_field_endpoint_validation_error(client: TestClient):
    """Test PATCH project field returns 422 on missing form data."""


# --- Test PATCH /api/resume/project/{id}/point/{index} ---
@pytest.mark.asyncio
async def test_update_project_point_endpoint_success(client: TestClient, mock_update_project_point):
    """Test PATCH project point succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_update_project_point_endpoint_not_found(client: TestClient, mock_update_project_point_not_found):
    """Test PATCH project point returns 404 if project/point not found."""


@pytest.mark.asyncio
async def test_update_project_point_endpoint_out_of_range(
    client: TestClient, mock_update_project_point_out_of_range
):
    """Test PATCH project point returns 404 if index is out of range."""


@pytest.mark.asyncio
async def test_update_project_point_endpoint_server_error(client: TestClient, mock_update_project_point_error):
    """Test PATCH project point returns 500 on service error."""


@pytest.mark.asyncio
async def test_update_project_point_endpoint_validation_error(client: TestClient):
    """Test PATCH project point returns 422 on missing form data."""


# --- Test POST /api/resume/education ---
@pytest.mark.asyncio
async def test_add_education_endpoint_success(client: TestClient, mock_add_education, mock_get_or_create_resume):
    """Test POST education succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_add_education_endpoint_server_error(
    client: TestClient, mock_add_education_error, mock_get_or_create_resume
):
    """Test POST education returns 500 on service error."""


# --- Test DELETE /api/resume/education/{id} ---
@pytest.mark.asyncio
async def test_delete_education_endpoint_success(client: TestClient, mock_delete_education):
    """Test DELETE education succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_delete_education_endpoint_not_found(client: TestClient, mock_delete_education_not_found):
    """Test DELETE education returns 404 if not found."""


@pytest.mark.asyncio
async def test_delete_education_endpoint_server_error(client: TestClient, mock_delete_education_error):
    """Test DELETE education returns 500 on service error."""


# --- Test POST /api/resume/project ---
@pytest.mark.asyncio
async def test_add_project_endpoint_success(client: TestClient, mock_add_project, mock_get_or_create_resume):
    """Test POST project succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_add_project_endpoint_server_error(
    client: TestClient, mock_add_project_error, mock_get_or_create_resume
):
    """Test POST project returns 500 on service error."""


# --- Test DELETE /api/resume/project/{id} ---
@pytest.mark.asyncio
async def test_delete_project_endpoint_success(client: TestClient, mock_delete_project):
    """Test DELETE project succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_delete_project_endpoint_not_found(client: TestClient, mock_delete_project_not_found):
    """Test DELETE project returns 404 if not found."""


@pytest.mark.asyncio
async def test_delete_project_endpoint_server_error(client: TestClient, mock_delete_project_error):
    """Test DELETE project returns 500 on service error."""


# --- Test POST /api/resume/experience ---
@pytest.mark.asyncio
async def test_add_experience_endpoint_success(client: TestClient, mock_add_experience, mock_get_or_create_resume):
    """Test POST experience succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_add_experience_endpoint_server_error(
    client: TestClient, mock_add_experience_error, mock_get_or_create_resume
):
    """Test POST experience returns 500 on service error."""


# --- Test DELETE /api/resume/experience/{id} ---
@pytest.mark.asyncio
async def test_delete_experience_endpoint_success(client: TestClient, mock_delete_experience):
    """Test DELETE experience succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_delete_experience_endpoint_not_found(client: TestClient, mock_delete_experience_not_found):
    """Test DELETE experience returns 404 if not found."""


@pytest.mark.asyncio
async def test_delete_experience_endpoint_server_error(client: TestClient, mock_delete_experience_error):
    """Test DELETE experience returns 500 on service error."""
