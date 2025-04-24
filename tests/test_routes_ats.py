"""Test suite for ATS API endpoints (app.routes.ats)."""

import pytest
from fastapi.testclient import TestClient

# Note: Fixtures like client, mock_get_or_create_resume, mock_optimize_resume etc.
# would be defined in tests/conftest.py


# --- Test GET /api/ats/optimize ---
@pytest.mark.asyncio
async def test_ats_optimize_success(client: TestClient, mock_get_or_create_resume, mock_optimize_resume):
    """Test GET /api/ats/optimize succeeds (200 OK)."""


@pytest.mark.asyncio
async def test_ats_optimize_error_getting_resume(client: TestClient, mock_get_or_create_resume_error):
    """Test GET /api/ats/optimize returns 500 if initial resume fetch fails."""


@pytest.mark.asyncio
async def test_ats_optimize_error_during_optimization(
    client: TestClient, mock_get_or_create_resume, mock_optimize_resume_error
):
    """Test GET /api/ats/optimize returns 500 if optimization service fails."""
