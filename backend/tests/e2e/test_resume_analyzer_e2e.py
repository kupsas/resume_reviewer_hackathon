"""End-to-end tests for the resume analyzer API."""
import json
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
import os
from httpx import AsyncClient, ASGITransport
import io

# Sample data for testing
SAMPLE_RESUME = """
John Doe
Software Engineer

EXPERIENCE
Senior Developer at Tech Corp
- Led development of microservices architecture
- Improved system performance by 40%

EDUCATION
BS in Computer Science
University of Technology
"""

# Mock OpenAI before importing FastAPI app
with patch("openai.AsyncOpenAI"):
    from app.services.resume_analyzer.analyzer import ResumeAnalyzer

# Create test client
client = TestClient(app)

# Sample data
SAMPLE_JOB = """
Senior Software Engineer
Required Skills:
- Python, FastAPI
- Microservices architecture
- CI/CD experience
- Team leadership
"""

@pytest.fixture
def sample_resume():
    """Sample resume for testing."""
    return SAMPLE_RESUME

@pytest.fixture
def sample_job():
    """Sample job description for testing."""
    return SAMPLE_JOB

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "sections": {
                            "summary": "Strong software engineer",
                            "experience": "5 years of experience",
                            "education": "BS in Computer Science",
                            "skills": "Python, FastAPI, React"
                        },
                        "scores": {
                            "relevance": 8,
                            "completeness": 9,
                            "clarity": 7
                        },
                        "recommendations": [
                            "Add more details about projects",
                            "Highlight leadership experience"
                        ]
                    })
                }
            }
        ]
    }

@pytest.fixture
def mock_openai():
    """Mock OpenAI client responses."""
    mock_response = AsyncMock()
    mock_response.choices = [
        type('Choice', (), {'message': type('Message', (), {'content': json.dumps({
            "star": {"complete": True},
            "metrics": ["Increased efficiency by 30%"],
            "contribution": 0.8
        })})})
    ]

    mock_job_response = AsyncMock()
    mock_job_response.choices = [
        type('Choice', (), {'message': type('Message', (), {'content': json.dumps({
            "match_score": 85,
            "skills_match": {
                "matched_skills": ["Python", "FastAPI"],
                "missing_skills": ["Docker"],
                "score": 80
            },
            "experience_match": {
                "years_match": True,
                "level_match": True,
                "score": 90
            },
            "project_match": {
                "scale_match": 85
            }
        })})})
    ]

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock()
    mock_client.chat.completions.create.side_effect = [mock_response, mock_job_response]

    with patch("app.services.resume_analyzer.ResumeAnalyzer", autospec=True) as mock_analyzer:
        instance = mock_analyzer.return_value
        instance.analyze_resume = AsyncMock(return_value={
            "scores": {
                "starScore": 0.8,
                "metricsScore": 0.7,
                "contributionScore": 0.8,
                "overall": 75
            },
            "sections": [{
                "section": "EXPERIENCE",
                "star": {"complete": True},
                "metrics": ["Increased efficiency by 30%"],
                "contribution": 0.8
            }],
            "recommendations": [],
            "job_match": {
                "match_score": 85,
                "skills_match": {
                    "matched_skills": ["Python", "FastAPI"],
                    "missing_skills": ["Docker"],
                    "score": 80
                },
                "experience_match": {
                    "years_match": True,
                    "level_match": True,
                    "score": 90
                },
                "project_match": {
                    "scale_match": 85
                }
            },
            "job_recommendations": []
        })
        instance._analyze_section = AsyncMock(return_value={
            "star": {"complete": True},
            "metrics": ["Increased efficiency by 30%"],
            "contribution": 0.8
        })
        instance._analyze_job_match = AsyncMock(return_value={
            "match_score": 85,
            "skills_match": {
                "matched_skills": ["Python", "FastAPI"],
                "missing_skills": ["Docker"],
                "score": 80
            },
            "experience_match": {
                "years_match": True,
                "level_match": True,
                "score": 90
            },
            "project_match": {
                "scale_match": 85
            }
        })
        yield mock_analyzer

@pytest.fixture
def mock_file_extraction():
    """Mock file extraction methods to return sample resume text."""
    with patch("app.services.resume_analyzer.utils.file_utils.extract_text_from_pdf") as mock_pdf, \
         patch("app.services.resume_analyzer.utils.file_utils.extract_text_from_docx") as mock_docx:
        mock_pdf.return_value = SAMPLE_RESUME
        mock_docx.return_value = SAMPLE_RESUME
        yield mock_pdf, mock_docx

@pytest.fixture
def sync_client():
    """Create a synchronous test client for FastAPI app."""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Create an async test client for FastAPI app."""
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def setup_and_teardown_async_client(async_client):
    """Setup and teardown for async client."""
    yield
    await async_client.aclose()

def test_health_check(sync_client):
    """Test health check endpoint."""
    response = sync_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root(sync_client):
    """Test root endpoint."""
    response = sync_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_analyze_resume_text(async_client, mock_openai):
    """Test resume analysis with text input."""
    response = await async_client.post(
        "/api/resume/analyze",
        json={"resume_text": SAMPLE_RESUME, "job_description": SAMPLE_JOB}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "scores" in result
    assert "sections" in result
    assert "recommendations" in result

@pytest.mark.asyncio
async def test_analyze_resume_file(async_client, mock_file_extraction, mock_openai):
    """Test resume analysis with file upload."""
    # Create a sample PDF file
    file_content = io.BytesIO(b"%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Count 1/Kids[3 0 R]>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Resources<<>>/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 21>>stream\nBT\n/F1 12 Tf\n(Test) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000212 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n284\n%%EOF")
    files = {
        "file": ("test.pdf", file_content, "application/pdf")
    }
    data = {"job_description": SAMPLE_JOB}
    
    response = await async_client.post(
        "/api/resume/analyze/file",
        files=files,
        data=data
    )
    
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
    
    assert response.status_code == 200
    result = response.json()
    assert "scores" in result
    assert "sections" in result
    assert "recommendations" in result

@pytest.mark.asyncio
async def test_job_matching(async_client, mock_openai):
    """Test job matching functionality."""
    response = await async_client.post(
        "/api/resume/match",
        json={
            "resume_text": SAMPLE_RESUME,
            "job_description": SAMPLE_JOB
        }
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "scores" in result
    assert "sections" in result
    assert "recommendations" in result

@pytest.mark.asyncio
async def test_error_handling(async_client):
    """Test error handling for invalid inputs."""
    # Test empty resume
    response = await async_client.post(
        "/api/resume/analyze",
        json={"resume_text": "", "job_description": SAMPLE_JOB}
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Resume text cannot be empty"

    # Test missing required field
    response = await async_client.post(
        "/api/resume/analyze",
        json={"job_description": SAMPLE_JOB}
    )
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_concurrent_requests(async_client, mock_openai):
    """Test handling multiple concurrent requests."""
    async def make_request():
        return await async_client.post(
            "/api/resume/analyze",
            json={"resume_text": SAMPLE_RESUME, "job_description": SAMPLE_JOB}
        )
    
    # Make 3 concurrent requests
    responses = await asyncio.gather(*[make_request() for _ in range(3)])
    
    # Verify all responses
    for response in responses:
        assert response.status_code == 200
        result = response.json()
        assert "scores" in result
        assert "sections" in result
        assert "recommendations" in result

@pytest.mark.asyncio
async def test_large_input(async_client, mock_openai):
    """Test handling large input text."""
    large_text = "A" * 50000  # 50KB of text
    response = await async_client.post(
        "/api/resume/analyze",
        json={"resume_text": large_text, "job_description": SAMPLE_JOB}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "scores" in result
    assert "sections" in result
    assert "recommendations" in result

@pytest.mark.asyncio
async def test_unicode_handling(async_client, mock_openai):
    """Test handling unicode characters in input."""
    unicode_text = "Resume with unicode: 简历 📝 résumé"
    response = await async_client.post(
        "/api/resume/analyze",
        json={"resume_text": unicode_text, "job_description": SAMPLE_JOB}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "scores" in result
    assert "sections" in result
    assert "recommendations" in result

def create_test_file(filename: str, content: bytes) -> tuple:
    """Create a test file for upload testing."""
    temp_dir = Path("temp_test_files")
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / filename
    file_path.write_bytes(content)
    return (filename, file_path.open("rb"), "application/pdf")

# Remove the global client variable since we're using fixtures
client = None 