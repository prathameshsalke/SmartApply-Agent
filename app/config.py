from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
DEMO_DATA_DIR = APP_DIR / "demo_data"
RESULTS_DIR = BASE_DIR / "results"

DEFAULT_JOB_DESCRIPTION_PATH = DEMO_DATA_DIR / "job_description.txt"
DEFAULT_USER_PROFILE_PATH = DEMO_DATA_DIR / "demo_user.json"
DEFAULT_RESUME_DIR = DEMO_DATA_DIR / "resumes"
DEFAULT_RESULTS_PATH = RESULTS_DIR / "application_results.json"
