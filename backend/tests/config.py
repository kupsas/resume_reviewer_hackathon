from pathlib import Path

# Test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_RESUMES_DIR = TEST_DATA_DIR / "resumes"
TEST_JOB_DESCRIPTIONS_DIR = TEST_DATA_DIR / "job_descriptions"

# Test file paths
SAMPLE_PDF_RESUME = TEST_RESUMES_DIR / "sample_resume.pdf"
SAMPLE_DOCX_RESUME = TEST_RESUMES_DIR / "sample_resume.docx"
SAMPLE_JOB_DESCRIPTION = TEST_JOB_DESCRIPTIONS_DIR / "sample_job.txt"

# Test settings
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB 