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
    # Create an AsyncMock instance. You might need to configure its methods
    # (e.g., .execute(), .scalar(), .commit(), .refresh()) further based on test needs.
    return AsyncMock()


@pytest.fixture(scope="session")
def client():
    """Provides a FastAPI TestClient instance."""
    if fastapi_app:
        with TestClient(fastapi_app) as test_client:
            yield test_client
    else:
        pytest.skip("FastAPI app instance not found, skipping client-dependent tests.")
        yield None  # Yield None to avoid fixture resolution errors if skipped


# --- Sample Data Fixtures ---


@pytest.fixture(scope="function")
def valid_personal_info() -> Dict[str, Any]:
    """Provides a valid PersonalInfo data dictionary."""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe",
    }


@pytest.fixture(scope="function")
def valid_skill_set() -> Dict[str, Any]:
    """Provides a valid SkillSet data dictionary."""
    return {
        "technical": ["Python", "FastAPI", "SQL"],
        "soft": ["Communication", "Teamwork"],
    }


@pytest.fixture(scope="function")
def valid_experience() -> Dict[str, Any]:
    """Provides a single valid Experience data dictionary."""
    return {
        "id": 1,
        "title": "Software Engineer",
        "company": "Tech Corp",
        "start_date": "2020-01-01",
        "end_date": "2023-12-31",
        "location": "Anytown, USA",
        "points": ["Developed feature X", "Fixed bug Y"],
    }


@pytest.fixture(scope="function")
def valid_project() -> Dict[str, Any]:
    """Provides a single valid Project data dictionary."""
    return {
        "id": 1,
        "name": "Cool Project",
        "description": "A project description.",
        "points": ["Implemented API", "Wrote tests"],
    }


@pytest.fixture(scope="function")
def valid_education() -> Dict[str, Any]:
    """Provides a single valid Education data dictionary."""
    return {
        "id": 1,
        "institution": "University of Example",
        "degree": "B.S. Computer Science",
        "start_date": "2016-09-01",
        "end_date": "2020-05-31",
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
        "skill_set": valid_skill_set,
        "experience": valid_experience_list,
        "projects": valid_project_list,
        "education": valid_education_list,
    }


@pytest.fixture(scope="function")
def sample_resume_data_missing_sections() -> Dict[str, Any]:
    """Provides sample resume data with some sections missing."""
    return {
        "id": 2,
        "personal_info": {"name": "Jane Smith"},
    }  # Example, missing skills, exp etc.


@pytest.fixture(scope="function")
def default_resume(sample_resume_data) -> Dict[str, Any]:
    """Provides a default resume dictionary structure."""
    return sample_resume_data  # Or a more specific default if needed


@pytest.fixture(scope="function")
def existing_resume_data(sample_resume_data) -> Dict[str, Any]:
    """Provides data representing an existing resume."""
    return sample_resume_data


@pytest.fixture(scope="function")
def sample_resume_object():
    """Provides a mock SQLAlchemy Resume object (or dict if simpler)."""
    # Using dict for simplicity, replace with mock ORM object if needed
    return MagicMock()  # Or return a dict similar to sample_resume_data


@pytest.fixture(scope="function")
def sample_resume_object_missing_data():
    """Provides a mock SQLAlchemy Resume object missing optional fields."""
    # Using dict for simplicity
    return MagicMock()  # Or a dict missing keys


@pytest.fixture(scope="function")
def sample_education():
    """Provides a mock SQLAlchemy Education object (or dict)."""
    return MagicMock()  # Or return valid_education dict


@pytest.fixture(scope="function")
def sample_experience():
    """Provides a mock SQLAlchemy Experience object (or dict)."""
    return MagicMock()  # Or return valid_experience dict


@pytest.fixture(scope="function")
def sample_project():
    """Provides a mock SQLAlchemy Project object (or dict)."""
    return MagicMock()  # Or return valid_project dict


@pytest.fixture(scope="function")
def sample_project_with_points(valid_project):
    """Provides a mock SQLAlchemy Project object with points."""
    mock_proj = MagicMock()
    mock_proj.id = valid_project["id"]
    mock_proj.points = valid_project["points"][:]  # Return a copy
    return mock_proj  # Or return valid_project dict


@pytest.fixture(scope="function")
def sample_llm_response_content() -> str:
    """Provides a sample successful LLM response string."""
    # This should resemble the actual expected output format of your LLM
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
    return "Optimized Resume:\nPersonal Info:\nName: John Doe"  # Missing other parts


# --- Mock Fixtures (Services, External Calls) ---


# Generic Mock Factory
def _create_mock_fixture(is_async: bool = True, side_effect=None):
    mock_type = AsyncMock if is_async else MagicMock
    mock = mock_type()
    if side_effect:
        mock.side_effect = side_effect
    return mock


# Resume Service Mocks
@pytest.fixture(scope="function")
def mock_get_or_create_resume(sample_resume_data):
    return _create_mock_fixture(side_effect=lambda session: sample_resume_data)


@pytest.fixture(scope="function")
def mock_get_or_create_resume_error():
    return _create_mock_fixture(side_effect=Exception("DB Error"))


@pytest.fixture(scope="function")
def mock_update_personal_info():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_update_personal_info_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_update_personal_info_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_update_skills():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_update_skills_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_update_skills_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_update_education_field():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_update_education_field_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_update_education_field_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_update_experience_field():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_update_experience_field_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_update_experience_field_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_update_project_field():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_update_project_field_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_update_project_field_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_update_project_point():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_update_project_point_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_update_project_point_out_of_range():
    return _create_mock_fixture(side_effect=IndexError)  # Or NoResultFound depending on implementation


@pytest.fixture(scope="function")
def mock_update_project_point_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_add_education(valid_education):
    return _create_mock_fixture(side_effect=lambda session, resume_id: valid_education)


@pytest.fixture(scope="function")
def mock_add_education_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_delete_education():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_delete_education_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_delete_education_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_add_project(valid_project):
    return _create_mock_fixture(side_effect=lambda session, resume_id: valid_project)


@pytest.fixture(scope="function")
def mock_add_project_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_delete_project():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_delete_project_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_delete_project_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_add_experience(valid_experience):
    return _create_mock_fixture(side_effect=lambda session, resume_id: valid_experience)


@pytest.fixture(scope="function")
def mock_add_experience_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


@pytest.fixture(scope="function")
def mock_delete_experience():
    return _create_mock_fixture(side_effect=lambda *args, **kwargs: True)


@pytest.fixture(scope="function")
def mock_delete_experience_not_found():
    return _create_mock_fixture(side_effect=NoResultFound)


@pytest.fixture(scope="function")
def mock_delete_experience_error():
    return _create_mock_fixture(side_effect=Exception("Service error"))


# ATS Service Mocks
@pytest.fixture(scope="function")
def mock_optimize_resume(sample_resume_data):
    # Assume optimize_resume returns the optimized data dict
    optimized_data = sample_resume_data.copy()  # Modify as needed
    optimized_data["personal_info"]["name"] = "Optimized Name"
    return _create_mock_fixture(side_effect=lambda resume_data: optimized_data)


@pytest.fixture(scope="function")
def mock_optimize_resume_error():
    return _create_mock_fixture(side_effect=Exception("Optimization failed"))


# External Library Mocks (LiteLLM)
@pytest.fixture(scope="function")
def mock_litellm_acompletion(sample_llm_response_content):
    mock_response = AsyncMock()
    # Adjust structure based on how you access LiteLLM's response content
    mock_response.choices[0].message.content = sample_llm_response_content
    mock_acompletion = AsyncMock(return_value=mock_response)
    # Use patch to replace the actual litellm.acompletion
    with patch("app.services.ats.acompletion", new=mock_acompletion, create=True):  # Target where it's used
        yield mock_acompletion


@pytest.fixture(scope="function")
def mock_litellm_acompletion_error():
    mock_acompletion = AsyncMock(side_effect=Exception("LiteLLM API Error"))
    with patch("app.services.ats.acompletion", new=mock_acompletion, create=True):  # Target where it's used
        yield mock_acompletion
