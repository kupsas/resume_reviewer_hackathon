import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json
from app.main import app
from tests.config import (
    TEST_RESUMES_DIR,
    TEST_JOB_DESCRIPTIONS_DIR,
    SAMPLE_PDF_RESUME,
    SAMPLE_DOCX_RESUME,
    SAMPLE_JOB_DESCRIPTION
)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_resume_pdf():
    """Test resume analysis with a PDF file."""
    # Skip if test file doesn't exist
    if not SAMPLE_PDF_RESUME.exists():
        pytest.skip(f"Test file {SAMPLE_PDF_RESUME} not found")
    
    with open(SAMPLE_PDF_RESUME, "rb") as pdf_file:
        with open(SAMPLE_JOB_DESCRIPTION, "r") as job_file:
            job_description = job_file.read()
            
            files = {"resume_file": ("sample_resume.pdf", pdf_file, "application/pdf")}
            data = {"job_description": job_description}
            
            response = client.post("/api/resume/analyze", files=files, data=data)
            
            assert response.status_code == 200
            assert "analysis" in response.json()
            assert response.json()["status"] == "success"
            
            # Print the analysis results
            print("\n\n=== PDF Resume Analysis (with Job Description) ===")
            print(json.dumps(response.json()["analysis"], indent=2))
            print("============================================\n")

def test_analyze_resume_docx():
    """Test resume analysis with a DOCX file."""
    # Skip if test file doesn't exist
    if not SAMPLE_DOCX_RESUME.exists():
        pytest.skip(f"Test file {SAMPLE_DOCX_RESUME} not found")
    
    with open(SAMPLE_DOCX_RESUME, "rb") as docx_file:
        files = {"resume_file": ("sample_resume.docx", docx_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        
        response = client.post("/api/resume/analyze", files=files)
        
        assert response.status_code == 200
        assert "analysis" in response.json()
        assert response.json()["status"] == "success"

        # Print the analysis results
        print("\n\n=== DOCX Resume Analysis (without Job Description) ===")
        print(json.dumps(response.json()["analysis"], indent=2))
        print("============================================\n")

def test_invalid_file_type():
    """Test uploading an invalid file type."""
    files = {"resume_file": ("test.txt", b"test content", "text/plain")}
    response = client.post("/api/resume/analyze", files=files)
    
    assert response.status_code == 400
    assert "File must be PDF or DOCX format" in response.json()["detail"]

def test_analyze_resume_pdf_no_job():
    """Test resume analysis with a PDF file without job description."""
    # Skip if test file doesn't exist
    if not SAMPLE_PDF_RESUME.exists():
        pytest.skip(f"Test file {SAMPLE_PDF_RESUME} not found")
    
    with open(SAMPLE_PDF_RESUME, "rb") as pdf_file:
        files = {"resume_file": ("sample_resume.pdf", pdf_file, "application/pdf")}
        
        response = client.post("/api/resume/analyze", files=files)
        
        assert response.status_code == 200
        assert "analysis" in response.json()
        assert response.json()["status"] == "success"
        
        # Print the analysis results
        print("\n\n=== PDF Resume Analysis (without Job Description) ===")
        print(json.dumps(response.json()["analysis"], indent=2))
        print("============================================\n")

def test_analyze_sashank_resume():
    """Test resume analysis with Sashank's resume against the sample job description."""
    sashank_resume = TEST_RESUMES_DIR / "Sashank_Resume.pdf"
    
    # Skip if test file doesn't exist
    if not sashank_resume.exists():
        pytest.skip(f"Test file {sashank_resume} not found")
    
    with open(sashank_resume, "rb") as pdf_file:
        with open(SAMPLE_JOB_DESCRIPTION, "r") as job_file:
            job_description = job_file.read()
            
            files = {"resume_file": ("Sashank_Resume.pdf", pdf_file, "application/pdf")}
            data = {"job_description": job_description}
            
            response = client.post("/api/resume/analyze", files=files, data=data)
            
            assert response.status_code == 200
            assert "analysis" in response.json()
            assert response.json()["status"] == "success"
            
            # Print the analysis results with clear formatting
            print("\n")
            print("="*80)
            print("RESUME ANALYSIS RESULTS")
            print("="*80)
            print("\nAnalyzing: Sashank_Resume.pdf")
            print("\nJob Description: Software Engineer Position")
            print("\nAnalysis Output:")
            print("-"*80)
            # Pretty print the JSON with proper indentation
            analysis = response.json()["analysis"]
            # Split the analysis by sections and print each section clearly
            sections = analysis.split("\n\n")
            for section in sections:
                print(f"\n{section.strip()}") 