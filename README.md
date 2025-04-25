# ResumeLM - AI-Powered Resume Builder

[![Python CI](https://github.com/anywaifu/auto-resume/actions/workflows/ci.yml/badge.svg)](https://github.com/anywaifu/auto-resume/actions/workflows/ci.yml)

ResumeLM is a web application designed to help users build and optimize their resumes with the assistance of AI. It features a dynamic web interface built with FastAPI and HTMX, allowing for interactive editing and real-time previews. The application integrates with Large Language Models (LLMs) via LLM to provide ATS (Applicant Tracking System) optimization suggestions.

## Features

*   **Interactive Resume Editor:** Edit personal info, skills, work experience, projects, and education sections.
*   **Real-time Preview:** See changes reflected instantly in the resume preview panel.
*   **HTMX Powered:** Dynamic UI updates without full page reloads.
*   **AI-Powered ATS Optimization:** Leverage LLMs (via Llamaindex) to get suggestions for improving resume content for ATS compatibility.
*   **SQLite Database:** Stores resume data persistently.
*   **Dockerized:** Easy setup and deployment using Docker and Docker Compose.
*   **Modular Codebase:** Services layer for business logic, FastAPI routes for API endpoints.

## Tech Stack

*   **Backend:** Python, FastAPI
*   **Frontend:** HTML, Tailwind CSS, HTMX, JavaScript (minimal)
*   **Database:** SQLite, SQLAlchemy (ORM)
*   **AI Integration:** OpenAI and Llamaindex
*   **Containerization:** Docker, Docker Compose
*   **Linting/Formatting:** Flake8, Black, isort, autoflake
*   **Testing:** Pytest

## Getting Started

### Prerequisites

*   Python 3.10+
*   Docker and Docker Compose
*   Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/anywaifu/auto-resume.git
    cd auto-resume
    ```
2.  **Create Environment File:**
    Copy the example environment file and configure your LLM settings:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and add your API keys for the desired LLM provider (e.g., `OPENAI_API_KEY`). Make sure the `DEFAULT_LLM_MODEL` variable matches a model identifier supported by OpenAI.

3.  **Build and Run with Docker Compose:**
    This is the recommended way to run the application.
    ```bash
    docker-compose up --build
    ```
    This command will:
    *   Build the Docker image using the `Dockerfile`.
    *   Start the `web` service defined in `docker-compose.yml`.
    *   Mount your local code for hot-reloading during development (if using bind mounts) or use named volumes.
    *   Load environment variables from your `.env` file.
    *   Persist the SQLite database (`resume.db`) in the project root.

### Accessing the Application

Once the containers are running, open your web browser and navigate to:
`http://localhost:8000`

## Development

### Running Locally (Without Docker)

1.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ensure your `.env` file is configured (see Installation).
4.  Run the FastAPI development server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Running Tests
bash
make test

### Linting and Formatting

*   Check for linting errors:
    ```bash
    make lint
    ```
*   Automatically format code and fix imports:
    ```bash
    make fix
    ```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.