"""Configuration and fixtures for the pytest test suite."""

from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.orm.exc import NoResultFound

from app.main import app as fastapi_app


@pytest_asyncio.fixture(scope="function")
async def mock_session():
    """Provides a mocked asynchronous SQLAlchemy session."""
    return AsyncMock()


@pytest.fixture(scope="session")
def client():
    """Provides a FastAPI TestClient instance."""
    if fastapi_app:
        with TestClient(fastapi_app) as test_client:
            yield test_client
    else:
        pytest.skip("FastAPI app instance not found, skipping client-dependent tests.")
        yield None


@pytest.fixture(scope="function")
def valid_personal_info() -> Dict[str, Any]:
    """Provides a valid PersonalInfo data dictionary."""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe",
        "location": "Anytown, USA",
    }


@pytest.fixture(scope="function")
def valid_personal_info_incomplete() -> Dict[str, Any]:
    """Provides an incomplete PersonalInfo data dictionary (missing name)."""
    return {
        "email": "jane.doe@example.com",
        "phone": "987-654-3210",
        "linkedin": "linkedin.com/in/janedoe",
        "github": "github.com/janedoe",
        "location": "Otherville, USA",
    }


@pytest.fixture(scope="function")
def valid_skill_set() -> Dict[str, Any]:
    """Provides a valid SkillSet data dictionary."""
    return {
        "technical_skills": "Python, FastAPI, SQL, React, Vue",
        "soft_skills": "Communication, Teamwork",
        "tools": "Git, Docker, Kubernetes",
    }


@pytest.fixture(scope="function")
def invalid_skill_set_type_data() -> Dict[str, Any]:
    """Provides SkillSet data with an invalid type for a field."""
    return {
        "technical_skills": 123,  # Invalid type
        "soft_skills": "Communication",
        "tools": "Git",
    }


@pytest.fixture(scope="function")
def valid_experience() -> Dict[str, Any]:
    """Provides a single valid Experience data dictionary."""
    return {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Anytown, USA",
        "start_date": "2020-01-01",
        "end_date": "2023-12-31",
        "description": "Developed feature X. Fixed bug Y.",
    }


@pytest.fixture(scope="function")
def missing_experience_field_data() -> Dict[str, Any]:
    """Provides Experience data missing a required field (title)."""
    return {
        "company": "Tech Corp",
        "location": "Anytown, USA",
        "start_date": "2020-01-01",
        "end_date": "2023-12-31",
        "description": "Developed feature X. Fixed bug Y.",
    }


@pytest.fixture(scope="function")
def invalid_experience_type_data() -> Dict[str, Any]:
    """Provides Experience data with an invalid type (start_date)."""
    return {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Anytown, USA",
        "start_date": 20200101,
        "end_date": "2023-12-31",
        "description": "Developed feature X. Fixed bug Y.",
    }


@pytest.fixture(scope="function")
def experience_data_optional_location_absent() -> Dict[str, Any]:
    """Provides Experience data without the optional location field."""
    return {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "start_date": "Jan 2020",
        "end_date": "Present",
        "description": "Developed feature X.",
    }


@pytest.fixture(scope="function")
def valid_project() -> Dict[str, Any]:
    """Provides a single valid Project data dictionary."""
    return {
        "name": "Cool Project",
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "description": "Implemented API and wrote tests.",
    }


@pytest.fixture(scope="function")
def missing_project_field_data() -> Dict[str, Any]:
    """Provides Project data missing a required field (name)."""
    return {
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "description": "Implemented API and wrote tests.",
    }


@pytest.fixture(scope="function")
def invalid_project_type_data() -> Dict[str, Any]:
    """Provides Project data with an invalid type (points)."""
    return {
        "name": "Cool Project",
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "description": ["This should be a string"],  # Invalid type for description
    }


@pytest.fixture(scope="function")
def invalid_project_description_type_data() -> Dict[str, Any]:
    """Provides Project data with description having the wrong type."""
    return {
        "name": "Cool Project",
        "url": "github.com/johndoe/coolproject",
        "technologies": "Python, FastAPI",
        "description": 12345,  # Invalid type for description
    }


@pytest.fixture(scope="function")
def valid_education() -> Dict[str, Any]:
    """Provides a single valid Education data dictionary."""
    return {
        "institution": "University of Example",
        "degree": "B.S. Computer Science",
        "graduation_date": "May 2020",
    }


@pytest.fixture(scope="function")
def missing_education_field_data() -> Dict[str, Any]:
    """Provides Education data missing a required field (institution)."""
    return {"degree": "B.S. Computer Science", "graduation_date": "May 2020"}


@pytest.fixture(scope="function")
def invalid_education_type_data() -> Dict[str, Any]:
    """Provides Education data with an invalid type (degree)."""
    return {
        "institution": "University of Example",
        "degree": 12345,
        "graduation_date": "May 2020",
    }


@pytest.fixture(scope="function")
def valid_experience_list(valid_experience) -> List[Dict[str, Any]]:
    """Provides a list containing valid Experience data."""
    return [valid_experience]


@pytest.fixture(scope="function")
def valid_project_list(valid_project) -> List[Dict[str, Any]]:
    """Provides a list containing valid Project data."""
    return [valid_project]


@pytest.fixture(scope="function")
def valid_education_list(valid_education) -> List[Dict[str, Any]]:
    """Provides a list containing valid Education data."""
    return [valid_education]


@pytest.fixture(scope="function")
def sample_resume_data(
    valid_personal_info,
    valid_skill_set,
    valid_experience_list,
    valid_project_list,
    valid_education_list,
) -> Dict[str, Any]:
    """Provides a dictionary representing sample resume data for service tests."""
    return {
        "id": 1,
        "personal_info": valid_personal_info,
        "skills": valid_skill_set,
        "experience": valid_experience_list,
        "projects": valid_project_list,
        "education": valid_education_list,
    }


@pytest.fixture(scope="function")
def missing_resume_section_data() -> Dict[str, Any]:
    """Provides resume data missing a required section (personal_info)."""
    return {
        "name": "My Incomplete Resume",
        "skills": {
            "programming_languages": "Python",
            "frameworks": "FastAPI",
            "developer_tools": "Docker",
        },
        "experience": [],
        "projects": [],
        "education": [],
    }


@pytest.fixture(scope="function")
def invalid_resume_data_section_type(
    valid_personal_info,
    valid_experience_list,
    valid_project_list,
    valid_education_list,
) -> Dict[str, Any]:
    """Provides Resume data where a section has an invalid type (skills as string)."""
    return {
        "personal_info": valid_personal_info,
        "skills": "This should be a SkillSet object/dict",
        "experience": valid_experience_list,
        "projects": valid_project_list,
        "education": valid_education_list,
    }


@pytest.fixture(scope="function")
def valid_ai_points_request() -> Dict[str, Any]:
    """Provides valid AIPointsRequest data."""
    return {
        "context": "Project X description",
        "num_points": 3,
        "job_title": "Software Engineer",
        "company": "Tech Company",
    }


@pytest.fixture(scope="function")
def valid_ai_enhance_data() -> Dict[str, str]:
    """Provides valid data for AIEnhanceRequest."""
    return {"text": "Enhance this: Developed feature X"}


@pytest.fixture(scope="function")
def invalid_ai_enhance_type_data() -> Dict[str, Any]:
    """Provides invalid data type for AIEnhanceRequest."""
    return {"text": 123}


@pytest.fixture(scope="function")
def incomplete_ai_points_request() -> Dict[str, Any]:
    """Provides incomplete AIPointsRequest data."""
    return {"context": "Some context only"}


@pytest.fixture(scope="function")
def invalid_ai_points_type_context_data() -> Dict[str, Any]:
    """Provides AIPointsRequest data with invalid context type."""
    return {"context": ["list"], "num_points": 3, "job_title": "Dev", "company": "Corp"}


@pytest.fixture(scope="function")
def invalid_ai_points_type_num_data() -> Dict[str, Any]:
    """Provides AIPointsRequest data with invalid num_points type."""
    return {"context": "Project X", "num_points": "five", "job_title": "Dev", "company": "Corp"}


@pytest.fixture(scope="function")
def sample_resume_data_missing_sections() -> Dict[str, Any]:
    """Provides sample resume data with some sections missing."""
    return {
        "id": 2,
        "personal_info": {"name": "Jane Smith"},
    }


@pytest.fixture(scope="function")
def default_resume(sample_resume_data) -> Dict[str, Any]:
    """Provides a default resume dictionary structure."""
    return sample_resume_data


@pytest.fixture(scope="function")
def existing_resume_data(sample_resume_data) -> Dict[str, Any]:
    """Provides data representing an existing resume."""
    return sample_resume_data


def _create_mock_db_object(data: Dict[str, Any]) -> MagicMock:
    """Helper to create a MagicMock simulating a DB object from a dict."""
    mock_obj = MagicMock()
    for key, value in data.items():
        setattr(mock_obj, key, value)
    mock_obj.__dict__.update(data)
    return mock_obj


@pytest.fixture(scope="function")
def sample_education_object(valid_education):
    """Provides a mock SQLAlchemy Education object configured with valid data."""
    data_with_id = valid_education.copy()
    data_with_id["id"] = 1
    return _create_mock_db_object(data_with_id)


@pytest.fixture(scope="function")
def sample_experience_object(valid_experience):
    """Provides a mock SQLAlchemy Experience object configured with valid data."""
    data_with_id = valid_experience.copy()
    data_with_id["id"] = 1
    return _create_mock_db_object(data_with_id)


@pytest.fixture(scope="function")
def sample_project_object(valid_project):
    """Provides a mock SQLAlchemy Project object configured with valid data."""
    data_with_id = valid_project.copy()
    data_with_id["id"] = 1
    return _create_mock_db_object(data_with_id)


@pytest.fixture(scope="function")
def sample_project_with_description(valid_project):
    """Provides a mock SQLAlchemy Project object with an ID and description."""
    data = valid_project.copy()
    # Ensure description is a string if it exists
    # No specific manipulation needed here for description as it's already a string
    return _create_mock_db_object(data)


@pytest.fixture(scope="function")
def sample_resume_object(sample_resume_data):
    """Provides a mock SQLAlchemy Resume object configured with nested data."""
    return _create_mock_db_object(sample_resume_data)


@pytest.fixture(scope="function")
def sample_resume_object_missing_data(sample_resume_data_missing_sections):
    """Provides a mock SQLAlchemy Resume object missing optional fields."""
    return _create_mock_db_object(sample_resume_data_missing_sections)


@pytest.fixture(scope="function")
def sample_llm_response_content() -> str:
    """Provides a sample successful LLM response string."""
    return """
    Optimized Resume:
    ... (formatted optimized resume sections) ...
    """


@pytest.fixture(scope="function")
def malformed_llm_response_content() -> str:
    """Provides a malformed LLM response string."""
    return "Sorry, I couldn't process that."


@pytest.fixture(scope="function")
def llm_response_missing_sections() -> str:
    """Provides an LLM response string missing expected sections."""
    return "Optimized Resume:\nPersonal Info:\nName: John Doe"


def _create_mock_fixture(is_async: bool = True, side_effect=None):
    mock_type = AsyncMock if is_async else MagicMock
    mock = mock_type()
    if side_effect:
        mock.side_effect = side_effect
    return mock


@pytest.fixture(scope="function")
def mock_get_or_create_resume(sample_resume_data):
    return _create_mock_fixture(side_effect=lambda session: sample_resume_data)


@pytest.fixture(scope="function")
def mock_get_or_create_resume_error():
    return _create_mock_fixture(side_effect=Exception("DB Error"))


@pytest.fixture(scope="function")
def mock_optimize_resume(sample_resume_data):
    optimized_data = sample_resume_data.copy()
    optimized_data["personal_info"]["name"] = "Optimized Name"  # Example modification
    return _create_mock_fixture(side_effect=lambda resume_data: optimized_data)


@pytest.fixture(scope="function")
def mock_optimize_resume_error():
    return _create_mock_fixture(side_effect=Exception("Optimization failed"))


@pytest.fixture(scope="function")
def mock_litellm_acompletion(sample_llm_response_content):
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = sample_llm_response_content
    mock_acompletion = AsyncMock(return_value=mock_response)
    with patch("app.services.ats.acompletion", new=mock_acompletion, create=True):
        yield mock_acompletion


@pytest.fixture(scope="function")
def mock_litellm_acompletion_error():
    mock_acompletion = AsyncMock(side_effect=Exception("LiteLLM API Error"))
    with patch("app.services.ats.acompletion", new=mock_acompletion, create=True):
        yield mock_acompletion


@pytest.fixture(scope="function")
def mock_update_personal_info():
    return _create_mock_fixture(side_effect=lambda session, resume_id, field, value: True)


@pytest.fixture(scope="function")
def mock_update_personal_info_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Personal info not found"))


@pytest.fixture(scope="function")
def mock_update_personal_info_error():
    return _create_mock_fixture(side_effect=Exception("DB update error"))


@pytest.fixture(scope="function")
def mock_update_skills():
    return _create_mock_fixture(side_effect=lambda session, resume_id, field, value: True)


@pytest.fixture(scope="function")
def mock_update_skills_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Skills not found"))


@pytest.fixture(scope="function")
def mock_update_skills_error():
    return _create_mock_fixture(side_effect=Exception("DB update error"))


@pytest.fixture(scope="function")
def mock_update_education_field():
    return _create_mock_fixture(side_effect=lambda session, edu_id, field, value: True)


@pytest.fixture(scope="function")
def mock_update_education_field_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Education not found"))


@pytest.fixture(scope="function")
def mock_update_education_field_error():
    return _create_mock_fixture(side_effect=Exception("DB update error"))


@pytest.fixture(scope="function")
def mock_add_education(sample_education_object):
    return _create_mock_fixture(
        side_effect=lambda session, resume_id: _create_mock_db_object(sample_education_object.__dict__)
    )


@pytest.fixture(scope="function")
def mock_add_education_error():
    return _create_mock_fixture(side_effect=Exception("DB add error"))


@pytest.fixture(scope="function")
def mock_delete_education():
    return _create_mock_fixture(side_effect=lambda session, edu_id: True)


@pytest.fixture(scope="function")
def mock_delete_education_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Education not found"))


@pytest.fixture(scope="function")
def mock_delete_education_error():
    return _create_mock_fixture(side_effect=Exception("DB delete error"))


@pytest.fixture(scope="function")
def mock_update_experience_field():
    return _create_mock_fixture(side_effect=lambda session, exp_id, field, value: True)


@pytest.fixture(scope="function")
def mock_update_experience_field_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Experience not found"))


@pytest.fixture(scope="function")
def mock_update_experience_field_error():
    return _create_mock_fixture(side_effect=Exception("DB update error"))


@pytest.fixture(scope="function")
def mock_add_experience(sample_experience_object):
    return _create_mock_fixture(
        side_effect=lambda session, resume_id: _create_mock_db_object(sample_experience_object.__dict__)
    )


@pytest.fixture(scope="function")
def mock_add_experience_error():
    return _create_mock_fixture(side_effect=Exception("DB add error"))


@pytest.fixture(scope="function")
def mock_delete_experience():
    return _create_mock_fixture(side_effect=lambda session, exp_id: True)


@pytest.fixture(scope="function")
def mock_delete_experience_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Experience not found"))


@pytest.fixture(scope="function")
def mock_delete_experience_error():
    return _create_mock_fixture(side_effect=Exception("DB delete error"))


@pytest.fixture(scope="function")
def mock_update_project_field():
    return _create_mock_fixture(side_effect=lambda session, res_id, proj_id, field, value: True)


@pytest.fixture(scope="function")
def mock_update_project_field_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Project not found"))


@pytest.fixture(scope="function")
def mock_update_project_field_error():
    return _create_mock_fixture(side_effect=Exception("DB update error"))


@pytest.fixture(scope="function")
def mock_update_project_point():
    return _create_mock_fixture(side_effect=lambda session, res_id, proj_id, idx, value: True)


@pytest.fixture(scope="function")
def mock_update_project_point_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Project point not found"))


@pytest.fixture(scope="function")
def mock_update_project_point_out_of_range():
    return _create_mock_fixture(side_effect=NoResultFound("Index out of range"))


@pytest.fixture(scope="function")
def mock_update_project_point_error():
    return _create_mock_fixture(side_effect=Exception("DB update error"))


@pytest.fixture(scope="function")
def mock_add_project(sample_project_object):
    return _create_mock_fixture(
        side_effect=lambda session, resume_id: _create_mock_db_object(sample_project_object.__dict__)
    )


@pytest.fixture(scope="function")
def mock_add_project_error():
    return _create_mock_fixture(side_effect=Exception("DB add error"))


@pytest.fixture(scope="function")
def mock_delete_project():
    return _create_mock_fixture(side_effect=lambda session, proj_id: True)


@pytest.fixture(scope="function")
def mock_delete_project_not_found():
    return _create_mock_fixture(side_effect=NoResultFound("Project not found"))


@pytest.fixture(scope="function")
def mock_delete_project_error():
    return _create_mock_fixture(side_effect=Exception("DB delete error"))
