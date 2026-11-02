# SmartApply-Agent

SmartApply-Agent is an AI-powered job application assistant that helps a candidate:
- analyze a job description
- compare multiple resumes against the role
- select the best-fit resume using ATS scoring
- fill application details from a candidate profile
- track application outcome in a master result file
- handle missing information and alert the user when something needs attention

This project is designed as a working MVP and demo-ready prototype for the "AI job application agent" idea.

## Features

- Resume parsing from text files
- ATS matching engine for job-description vs resume comparison
- Demo candidate profile with personal details, education, skills, and experience
- Auto-selection of the best-fit resume
- Simulated browser-based form filling workflow
- Application result tracker in JSON/CSV format
- Demo job description and sample resumes
- Optional FastAPI endpoint for automation integration

## Project structure

```text
SmartApply-Agent/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── demo_data/
│   │   ├── demo_user.json
│   │   ├── job_description.txt
│   │   └── resumes/
│   │       ├── resume_python_backend.txt
│   │       ├── resume_data_analyst.txt
│   │       └── resume_frontend_developer.txt
│   └── utils/
│       ├── __init__.py
│       ├── application_tracker.py
│       ├── ats_matcher.py
│       ├── form_filler.py
│       └── resume_parser.py
├── .gitignore
├── README.md
├── requirements.txt
└── results/
    └── application_results.json
```

## Demo user included

A sample candidate profile has already been created:
- Full name: Priya Sharma
- Email: priya.sharma@gmail.com
- Phone: +1 415-555-0102
- Education: B.Tech in Computer Science
- Experience: 3 years
- Skills: Python, FastAPI, SQL, REST APIs, Docker, JavaScript, React
- Roles: Python Developer, Backend Engineer, Full Stack Developer

## Demo job

The demo job description is for a Python backend engineer role requiring:
- Python
- FastAPI
- SQL
- REST APIs
- Flask or Django
- AWS
- Docker
- CI/CD
- communication and problem solving

## Quick start

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. Run the demo application:

```bash
python -m app.main
```

This will:
- load the demo user profile
- scan all sample resumes
- score each resume against the job description
- choose the best resume
- simulate form filling and application submission
- save the output to `results/application_results.json`

5. Optionally run the API:

```bash
uvicorn app.api:app --reload
```

Then call the endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/apply" \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://example.com/jobs/python-backend-engineer",
    "company_name": "Nova Systems",
    "job_title": "Python Backend Engineer",
    "job_description": "We are hiring a Python backend engineer with FastAPI, SQL, REST APIs, Docker, and CI/CD experience.",
    "candidate": {
      "full_name": "Priya Sharma",
      "email": "priya.sharma@gmail.com",
      "phone": "+1 415-555-0102",
      "location": "San Francisco, CA",
      "gender": "female",
      "education": ["B.Tech in Computer Science"],
      "experience_years": 3,
      "skills": ["Python", "FastAPI", "SQL", "REST APIs", "Docker", "JavaScript"],
      "preferred_roles": ["Python Developer", "Backend Engineer"]
    }
  }'
```

## Output example

The application result includes:
- selected resume
- ATS score
- matched keywords
- missing keywords
- filled form fields
- application status
- warnings

## Notes

This project is a realistic MVP for job-application automation, but it does not access live job portals or real browser automation by default. The form-filling step is simulated for demo purposes, while the project structure prepares the system for real Playwright/Selenium automation in a future stage.

## Future upgrade ideas

- Add real Playwright automation for website forms
- Connect to Google Sheets / Excel tracking
- Add resume upload from PDF/DOCX files
- Add user authentication and profile dashboard
- Add email notifications on failed or blocked application steps
- Support multiple jobs and candidate resume pools

## License

MIT
