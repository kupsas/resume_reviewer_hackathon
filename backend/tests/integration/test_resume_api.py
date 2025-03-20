"""Integration tests for the resume analysis API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import io
import json
from pathlib import Path
from app.main import app
from app.services.resume_analyzer import ResumeAnalyzer
from tests.config import (
    TEST_RESUMES_DIR,
    TEST_JOB_DESCRIPTIONS_DIR,
    SAMPLE_PDF_RESUME,
    SAMPLE_DOCX_RESUME,
    SAMPLE_JOB_DESCRIPTION
)

# Create a test client
client = TestClient(app)

# Sample test data
SAMPLE_RESUME_TEXT = """
EXPERIENCE
Software Engineer at Tech Corp (2020-Present)
- Led development of microservices architecture
- Improved system performance by 40%

EDUCATION
BS in Computer Science, University of Tech (2016-2020)
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer
Requirements:
- 5+ years of experience in Python
- Experience with microservices
"""

def validate_resume_analysis(analysis):
    """Helper function to validate the structure of resume analysis."""
    assert "status" in analysis
    assert analysis["status"] == "success"
    
    assert "resumeAnalysis" in analysis
    resume_analysis = analysis["resumeAnalysis"]
    
    # Validate sections array
    assert "sections" in resume_analysis
    assert isinstance(resume_analysis["sections"], list)
    
    # Validate each section
    for section in resume_analysis["sections"]:
        assert "type" in section
        assert "points" in section
        
        # Validate points in each section
        for point in section["points"]:
            assert "text" in point
            assert "star" in point
            assert "metrics" in point
            assert "technical_score" in point
            assert "improvement" in point

def validate_job_match(analysis):
    """Helper function to validate job match analysis structure."""
    assert "jobMatchAnalysis" in analysis
    job_match = analysis["jobMatchAnalysis"]
    
    # Validate match score
    assert "match_score" in job_match
    assert isinstance(job_match["match_score"], (int, float))
    
    # Validate technical match
    assert "technical_match" in job_match
    tech_match = job_match["technical_match"]
    assert "matched_skills" in tech_match
    assert "missing_skills" in tech_match
    assert "skill_coverage_score" in tech_match
    
    # Validate experience match
    assert "experience_match" in job_match
    exp_match = job_match["experience_match"]
    assert "required_years" in exp_match
    assert "actual_years" in exp_match
    assert "experience_score" in exp_match
    
    # Validate key requirements
    assert "key_requirements" in job_match
    key_reqs = job_match["key_requirements"]
    assert "met" in key_reqs
    assert "partially_met" in key_reqs
    assert "not_met" in key_reqs
    
    # Validate recommendations
    assert "section_recommendations" in job_match
    assert "recommendations" in job_match

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response."""
    return {
        "status": "success",
        "resumeAnalysis": {
            "sections": [
                {
                    "type": "EXPERIENCE",
                    "points": [
                        {
                            "text": "Led development of microservices architecture",
                            "star": {
                                "situation": True,
                                "task": True,
                                "action": True,
                                "result": True,
                                "complete": True
                            },
                            "metrics": ["40% improvement"],
                            "technical_score": 4.0,
                            "improvement": "Enhanced suggestion"
                        }
                    ]
                }
            ]
        },
        "jobMatchAnalysis": {
            "match_score": 85,
            "technical_match": {
                "matched_skills": ["Python", "Microservices"],
                "missing_skills": ["Kubernetes"],
                "skill_coverage_score": 80
            },
            "experience_match": {
                "required_years": 5,
                "actual_years": 3,
                "experience_score": 75
            },
            "key_requirements": {
                "met": ["Python experience"],
                "partially_met": ["Years of experience"],
                "not_met": ["Kubernetes experience"]
            },
            "section_recommendations": {
                "experience_projects": [
                    {
                        "original_point": "Led development",
                        "improved_version": "Led development with metrics"
                    }
                ],
                "education": "Add relevant coursework",
                "skills_certs": "Add cloud certifications"
            },
            "recommendations": ["Add Kubernetes experience"]
        },
        "tokenUsage": {
            "total_tokens": 100,
            "prompt_tokens": 50,
            "completion_tokens": 50,
            "total_cost": 0.002
        }
    }

@pytest.fixture
def mock_pdf_file():
    """Create a mock PDF file."""
    return io.BytesIO(b"%PDF-1.4\nMock PDF content")

@pytest.fixture
def mock_docx_file():
    """Create a mock DOCX file."""
    return io.BytesIO(b"Mock DOCX content")

@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_analyze_resume_text(mock_openai_response):
    """Test the /analyze endpoint with resume text."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze:
        mock_analyze.return_value = mock_openai_response
        
        response = client.post(
            "/api/resume/analyze",
            json={"resume_text": SAMPLE_RESUME_TEXT}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_resume_analysis(data)

@pytest.mark.asyncio
async def test_analyze_resume_with_job(mock_openai_response):
    """Test the /analyze endpoint with resume text and job description."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze, \
         patch("app.services.openai_service.OpenAIService.analyze_job_match") as mock_job_match:
        
        mock_analyze.return_value = mock_openai_response
        mock_job_match.return_value = mock_openai_response
        
        response = client.post(
            "/api/resume/analyze",
            json={
                "resume_text": SAMPLE_RESUME_TEXT,
                "job_description": SAMPLE_JOB_DESCRIPTION
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_resume_analysis(data)
        validate_job_match(data)

@pytest.mark.asyncio
async def test_analyze_resume_file(mock_openai_response, mock_pdf_file):
    """Test the /analyze/file endpoint with a PDF file."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze:
        mock_analyze.return_value = mock_openai_response
        
        response = client.post(
            "/api/resume/analyze/file",
            files={"file": ("resume.pdf", mock_pdf_file, "application/pdf")}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_resume_analysis(data)

@pytest.mark.asyncio
async def test_analyze_resume_file_with_job(mock_openai_response, mock_pdf_file):
    """Test the /analyze/file endpoint with a PDF file and job description."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze, \
         patch("app.services.openai_service.OpenAIService.analyze_job_match") as mock_job_match:
        
        mock_analyze.return_value = mock_openai_response
        mock_job_match.return_value = mock_openai_response
        
        response = client.post(
            "/api/resume/analyze/file",
            files={"file": ("resume.pdf", mock_pdf_file, "application/pdf")},
            data={"job_description": SAMPLE_JOB_DESCRIPTION}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_resume_analysis(data)
        validate_job_match(data)

@pytest.mark.asyncio
async def test_analyze_docx_file(mock_openai_response, mock_docx_file):
    """Test the /analyze/file endpoint with a DOCX file."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze:
        mock_analyze.return_value = mock_openai_response
        
        response = client.post(
            "/api/resume/analyze/file",
            files={"file": ("resume.docx", mock_docx_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_resume_analysis(data)

@pytest.mark.asyncio
async def test_invalid_file_type():
    """Test handling of invalid file types."""
    invalid_file = io.BytesIO(b"Invalid file content")
    
    response = client.post(
        "/api/resume/analyze/file",
        files={"file": ("resume.txt", invalid_file, "text/plain")}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Unsupported file type" in data["detail"]

@pytest.mark.asyncio
async def test_empty_resume_text():
    """Test handling of empty resume text."""
    response = client.post(
        "/api/resume/analyze",
        json={"resume_text": ""}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Empty resume text" in data["detail"]

@pytest.mark.asyncio
async def test_invalid_json():
    """Test handling of invalid JSON payload."""
    response = client.post(
        "/api/resume/analyze",
        json={"invalid_key": "value"}
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_rate_limit_headers(mock_openai_response):
    """Test presence of rate limit headers in response."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze:
        mock_analyze.return_value = mock_openai_response
        
        response = client.post(
            "/api/resume/analyze",
            json={"resume_text": SAMPLE_RESUME_TEXT}
        )
        
        assert response.status_code == 200
        assert "x-rate-limit-limit" in response.headers
        assert "x-rate-limit-remaining" in response.headers
        assert "x-rate-limit-reset" in response.headers

@pytest.mark.asyncio
async def test_openai_error_handling(mock_openai_response):
    """Test handling of OpenAI API errors."""
    with patch("app.services.openai_service.OpenAIService.analyze_resume_content") as mock_analyze:
        mock_analyze.side_effect = Exception("OpenAI API Error")
        
        response = client.post(
            "/api/resume/analyze",
            json={"resume_text": SAMPLE_RESUME_TEXT}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "OpenAI API Error" in str(data["detail"]) 