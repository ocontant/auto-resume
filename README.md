# ResumeLM - Self Hosted ATS Optimization Resume Editor

[![Python CI](https://github.com/anywaifu/auto-resume/actions/workflows/ci.yml/badge.svg)](https://github.com/anywaifu/auto-resume/actions/workflows/ci.yml)

ResumeLM is a self-hosted web application for creating, managing, and optimizing resumes for Applicant Tracking Systems (ATS) using AI. It provides a private, efficient way to tailor your resume for specific job applications and generate professional PDF outputs.

<!-- Placeholder for Resume Edit Page Screenshot -->
<div align="center">
  [INSERT RESUME EDIT SCREENSHOT HERE]
  <p><i>Fig 1: The resume editor interface with live preview.</i></p>
</div>

## ✨ Features

*   **📄 Resume Management:** Import existing PDF resumes or build new ones using a structured editor. Manage multiple resume versions.
*   **🤖 Smart ATS Optimization:**
    *   Utilizes AI (OpenAI models like GPT-4o Mini) to analyze your resume against a provided job description.
    *   Rewrites content to incorporate relevant keywords and phrasing, aiming to improve ATS compatibility.
    *   Allows customization of the AI's instructions (prompt) via the configuration settings.
*   **🚀 PDF Export:** Download the AI-optimized version of your resume as a clean, formatted PDF, ready for submission.
*   **⚙️ Web-Based Configuration:** Set your OpenAI API key, choose the AI model, and manage resume settings directly through the **config** page.

<!-- Placeholder for Config Page Screenshot -->
<div align="center">
  [INSERT CONFIG PAGE SCREENSHOT HERE]
  <p><i>Fig 2: Configuration page for AI settings and resume management.</i></p>
</div>

## 🚀 Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/anywaifu/auto-resume.git
    cd auto-resume
    ```
2.  **Launch with Docker:**
    (Requires Docker and Docker Compose)
    ```bash
    docker-compose up -d --build
    ```

3.  **Access ResumeLM:**
    Open your web browser to: `http://localhost:8010`

4.  **Initial Configuration:**
    *   Navigate to the **Config** page.
    *   Enter your **OpenAI API Key** in the "LLM Settings" section. This is required for PDF import parsing and ATS optimization.
    *   Select your preferred OpenAI model (e.g., `gpt-4o-mini`).
    *   Save the settings.

## 💻 Workflow (Import -> Configure -> Select -> Optimize & Download)

Follow these steps for efficient resume tailoring:

1.  **Import Resume:**
    *   Go to the **Config** page.
    *   Use the "Import Resume" section to upload your base resume PDF. Assign it a name.
    *   *(Tip: You can use the sample resume PDF located in the `sample/` folder if you don't have one handy).*
    *   The resume will appear in the "My Resumes" list on the right.
2.  **(Optional) Configure Optimization Settings:**
    *   **Provide Job Context:** While still on the **Config** page, paste the target **Job Description** into the "ATS Optimization" section and save. This helps the AI tailor the resume more specifically. *Optimization can also run without a job description set.*
    *   **Adjust AI Instructions:** Review the "Custom ATS Prompt" on the Config page. Modify it if you want to change how the AI optimizes. *Note: The prompt should instruct the AI to generate HTML styled with pure inline CSS, as this ensures proper rendering in the exported PDF.* Save any changes. *The default prompt includes this instruction.*
3.  **Select & Review:**
    *   Now, in the "My Resumes" list on the Config page, click "Select" next to your resume. This takes you to the editor page.
    *   Review the parsed content across the different tabs (Basic Info, Work, Skills, etc.). Make any necessary edits; changes are saved automatically.
4.  **Optimize & Download:**
    *   Click the **"ATS Optimize"** button on the editor page.
    *   Wait for the AI to process and update the preview panel.
    *   Review the AI-enhanced resume content.
    *   Click the **"Download Optimized"** button (which becomes active after optimization) to get the tailored PDF.


## 🔧 Technical Details

*   **Backend:** Python / FastAPI
*   **Frontend:** HTMX / Tailwind CSS
*   **AI Integration:** OpenAI API via LlamaIndex
*   **PDF Handling:** WeasyPrint (Export - supports HTML + pure CSS) / PyMuPDF (Import)
*   **Database:** SQLite
*   **Deployment:** Docker / Docker Compose

## 🤝 Contributing

Contributions are welcome. Please fork the repository, create a feature branch, make your changes, ensure tests pass (`make test`), format your code (`make fix`), and open a Pull Request.

## 📄 License

MIT Licensed.
