# AutoResume AI - AST Repository Map

Generated using tree-sitter AST analysis

## Summary

- **Total Python Files**: 22
- **Total Classes**: 15
- **Total Functions**: 267
- **Total Methods**: 0

## Module Structure

### Package: `app`

#### `app.__init__`
*app/__init__.py*

---

#### `app.db`
*app/db.py*

**Imports:**
- Line 1: `import os`
- Line 2: `from datetime import datetime`
- Line 4: `from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine`
- Line 5: `from sqlalchemy.orm import declarative_base, relationship, sessionmaker`

**Classes:**
- `PersonalInfo` (line 19)
- `SkillSet` (line 34)
- `Education` (line 47)
- `Experience` (line 60)
- `Project` (line 76)
- `Resume` (line 90)
- `Config` (line 111)

**Functions:**
- `create_db_and_tables()` (line 122)
- `get_session()` (line 133)

---

#### `app.main`
*app/main.py*

**Imports:**
- Line 1: `from contextlib import asynccontextmanager`
- Line 3: `import uvicorn`
- Line 4: `from fastapi import Depends, FastAPI, HTTPException, Query, Request`
- Line 5: `from fastapi.responses import HTMLResponse, RedirectResponse`
- Line 6: `from fastapi.staticfiles import StaticFiles`
- ... and 8 more

**Functions:**
- `lifespan()` (line 19)
- `root()` (line 47)
- `home()` (line 60)

---

#### `app.models`
*app/models.py*

**Imports:**
- Line 1: `from typing import List, Optional`
- Line 3: `from pydantic import BaseModel, ConfigDict`

**Classes:**
- `PersonalInfo` (line 6)
- `SkillSet` (line 18)
- `Experience` (line 28)
- `Project` (line 41)
- `Education` (line 52)
- `Resume` (line 62)
- `AIEnhanceRequest` (line 74)
- `AIPointsRequest` (line 78)

**Functions:**
- `db_resume_to_dict()` (line 85)

---

#### `app.routes.__init__`
*app/routes/__init__.py*

---

#### `app.routes.ats`
*app/routes/ats.py*

**Imports:**
- Line 1: `from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response`
- Line 2: `from fastapi.templating import Jinja2Templates`
- Line 3: `from sqlalchemy.orm import Session`
- Line 4: `from weasyprint import HTML`
- Line 6: `from app.db import get_session`
- ... and 3 more

**Functions:**
- `get_optimized_resume()` (line 34)
- `download_ats_resume_pdf_from_html()` (line 48)

---

#### `app.routes.config`
*app/routes/config.py*

**Imports:**
- Line 1: `from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile`
- Line 2: `from fastapi.templating import Jinja2Templates`
- Line 3: `from sqlalchemy.exc import NoResultFound`
- Line 4: `from sqlalchemy.orm import Session`
- Line 6: `from app.db import get_session`
- ... and 3 more

**Functions:**
- `get_config_page()` (line 23)
- `import_resume()` (line 45)
- `delete_resume()` (line 64)
- `save_ats_settings_endpoint()` (line 74)
- `save_llm_settings_endpoint()` (line 93)
- `save_pdf_margin_endpoint()` (line 112)

---

#### `app.routes.resume`
*app/routes/resume.py*

**Imports:**
- Line 1: `from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response`
- Line 2: `from fastapi.templating import Jinja2Templates`
- Line 3: `from sqlalchemy.exc import NoResultFound`
- Line 4: `from sqlalchemy.orm import Session`
- Line 6: `from app.db import get_session`
- ... and 1 more

**Functions:**
- `get_personal_section()` (line 28)
- `get_experience_section()` (line 38)
- `get_skills_section()` (line 47)
- `get_education_section()` (line 56)
- `get_projects_section()` (line 66)
- `get_resume_preview()` (line 76)
- `update_personal_info_field()` (line 88)
- `update_skills_field_endpoint()` (line 103)
- `update_education_field_endpoint()` (line 118)
- `update_experience_field_endpoint()` (line 137)
- ... and 7 more functions

---

#### `app.services.__init__`
*app/services/__init__.py*

---

#### `app.services.ats`
*app/services/ats.py*

**Imports:**
- Line 1: `import json`
- Line 2: `from typing import Any, Dict`
- Line 4: `from dotenv import load_dotenv`
- Line 5: `from llama_index.core.llms import ChatMessage, MessageRole`
- Line 6: `from llama_index.llms.openai import OpenAI`
- ... and 4 more

**Functions:**
- `optimize_resume()` (line 16)
- `build_user_message()` (line 36)
- `_parse_llm_response()` (line 53)

---

#### `app.services.config`
*app/services/config.py*

**Imports:**
- Line 1: `import os`
- Line 2: `from typing import Optional`
- Line 4: `from sqlalchemy.orm import Session`
- Line 6: `from app.db import Config`

**Functions:**
- `get_default_ats_prompt()` (line 18)
- `get_config_value()` (line 50)
- `set_config_value()` (line 59)
- `get_ats_settings()` (line 72)
- `save_ats_settings()` (line 80)
- `get_llm_settings()` (line 86)
- `save_llm_settings()` (line 93)
- `get_pdf_page_margin()` (line 99)
- `save_pdf_page_margin()` (line 104)

---

#### `app.services.pdf_import`
*app/services/pdf_import.py*

**Imports:**
- Line 1: `import fitz`
- Line 2: `from llama_index.core.llms import ChatMessage`
- Line 3: `from llama_index.llms.openai import OpenAI`
- Line 4: `from sqlalchemy.orm import Session`
- Line 6: `from app.models import Resume`
- ... and 2 more

**Functions:**
- `extract_text_from_pdf()` (line 11)
- `parse_resume_text()` (line 24)
- `import_resume_from_pdf()` (line 56)

---

#### `app.services.resume`
*app/services/resume.py*

**Imports:**
- Line 1: `from typing import Any, Dict, List, Type`
- Line 3: `from sqlalchemy import update`
- Line 4: `from sqlalchemy.exc import NoResultFound`
- Line 5: `from sqlalchemy.orm import Session`
- Line 7: `from app.db import Education, Experience, PersonalInfo, Project, Resume, SkillSet`
- ... and 1 more

**Functions:**
- `get_resume_by_id()` (line 11)
- `get_resume_dict()` (line 19)
- `get_all_resumes()` (line 29)
- `create_resume()` (line 43)
- `update_entity_field()` (line 75)
- `update_personal_info()` (line 95)
- `update_skills()` (line 100)
- `update_education_field()` (line 105)
- `update_experience_field()` (line 119)
- `update_project_field()` (line 133)
- ... and 8 more functions

---

#### `app.utils.__init__`
*app/utils/__init__.py*

---

### Root Level Files

#### `generate_repomap`
*generate_repomap.py*

**Imports:**
- Line 4: `import os`
- Line 5: `from pathlib import Path`
- Line 6: `import tree_sitter_python as tspython`
- Line 7: `from tree_sitter import Language, Parser`
- Line 8: `import json`

**Functions:**
- `extract_python_structure()` (line 14)
- `traverse()` (line 28)
- `generate_repomap()` (line 79)
- `format_markdown_report()` (line 119)

---

### Package: `tests`

#### `tests.__init__`
*tests/__init__.py*

---

#### `tests.conftest`
*tests/conftest.py*

**Imports:**
- Line 3: `from typing import Any, Dict, List`
- Line 4: `from unittest.mock import AsyncMock, MagicMock, patch`
- Line 6: `import pytest`
- Line 7: `import pytest_asyncio`
- Line 8: `from fastapi.testclient import TestClient`
- ... and 2 more

**Functions:**
- `mock_session()` (line 15)
- `client()` (line 21)
- `valid_personal_info()` (line 32)
- `valid_personal_info_incomplete()` (line 45)
- `valid_skill_set()` (line 57)
- `invalid_skill_set_type_data()` (line 67)
- `valid_experience()` (line 77)
- `missing_experience_field_data()` (line 90)
- `invalid_experience_type_data()` (line 102)
- `experience_data_optional_location_absent()` (line 115)
- ... and 73 more functions

---

#### `tests.test_models`
*tests/test_models.py*

**Imports:**
- Line 1: `import pytest`
- Line 2: `from pydantic import ValidationError`
- Line 5: `from app.models import (
    AIEnhanceRequest,
    AIPointsRequest,
    Education,
    Experience,
    PersonalInfo,
    Project,
    Resume,
    SkillSet,
)`

**Functions:**
- `test_personal_info_valid()` (line 17)
- `test_personal_info_missing_field()` (line 27)
- `test_personal_info_invalid_type()` (line 35)
- `test_skill_set_valid()` (line 43)
- `test_skill_set_invalid_type()` (line 51)
- `test_experience_valid()` (line 57)
- `test_experience_missing_field()` (line 65)
- `test_experience_invalid_type()` (line 72)
- `test_experience_optional_location_absent()` (line 78)
- `test_project_valid()` (line 84)
- ... and 16 more functions

---

#### `tests.test_routes_ats`
*tests/test_routes_ats.py*

**Imports:**
- Line 3: `import pytest`
- Line 4: `from fastapi.testclient import TestClient`

**Functions:**
- `test_ats_optimize_success()` (line 12)
- `test_ats_optimize_error_getting_resume()` (line 17)
- `test_ats_optimize_error_during_optimization()` (line 22)

---

#### `tests.test_routes_resume`
*tests/test_routes_resume.py*

**Imports:**
- Line 3: `import pytest`
- Line 4: `from fastapi.testclient import TestClient`

**Functions:**
- `test_get_personal_section()` (line 12)
- `test_get_experience_section()` (line 17)
- `test_get_skills_section()` (line 22)
- `test_get_education_section()` (line 27)
- `test_get_projects_section()` (line 32)
- `test_update_personal_info_field_success()` (line 38)
- `test_update_personal_info_field_not_found()` (line 43)
- `test_update_personal_info_field_server_error()` (line 48)
- `test_update_personal_info_field_validation_error()` (line 53)
- `test_update_skills_field_success()` (line 59)
- ... and 35 more functions

---

#### `tests.test_services_ats`
*tests/test_services_ats.py*

**Imports:**
- Line 3: `import pytest`

**Functions:**
- `test_init_llm_configures_litellm_if_possible()` (line 10)
- `test_create_ats_prompt_structure()` (line 16)
- `test_create_ats_prompt_handles_missing_sections()` (line 20)
- `test_parse_llm_response_success()` (line 27)
- `test_parse_llm_response_handles_malformed_content()` (line 31)
- `test_parse_llm_response_handles_missing_sections_in_response()` (line 35)
- `test_optimize_resume_success()` (line 43)
- `test_optimize_resume_llm_api_error()` (line 48)
- `test_optimize_resume_parsing_error()` (line 53)
- `test_optimize_resume_error_getting_resume()` (line 60)

---

#### `tests.test_services_resume`
*tests/test_services_resume.py*

**Imports:**
- Line 3: `import pytest`

**Functions:**
- `test_get_resume_by_id_found()` (line 11)
- `test_get_resume_by_id_not_found()` (line 16)
- `test_get_or_create_default_resume_creates_new()` (line 22)
- `test_get_or_create_default_resume_returns_existing()` (line 27)
- `test_resume_to_dict_conversion()` (line 32)
- `test_resume_to_dict_handles_missing_optional_relations()` (line 36)
- `test_update_personal_info_success()` (line 44)
- `test_update_personal_info_not_found()` (line 49)
- `test_update_personal_info_invalid_field()` (line 54)
- `test_update_skills_success()` (line 60)
- ... and 22 more functions

---
