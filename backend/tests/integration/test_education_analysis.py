import pytest
from unittest.mock import MagicMock, AsyncMock
import json

from app.services.resume_analyzer import ResumeAnalyzer
from app.services.openai_service import OpenAIService

@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_completions = MagicMock()
    
    # Structure the mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                function_call=MagicMock(
                    arguments=json.dumps({
                        "sections": [
                            {
                                "type": "Education",
                                "points": [
                                    {
                                        "school": "Stanford University",
                                        "degree": "Bachelor of Science in Computer Science",
                                        "graduation_date": "2023",
                                        "gpa": "3.8",
                                        "coursework": ["Data Structures", "Algorithms", "Machine Learning"],
                                        "projects": ["Senior Thesis on AI Ethics"],
                                        "activities": ["ACM Club President"]
                                    }
                                ],
                                "reputation_score": 85,
                                "suggestions": ["Consider adding more details about academic achievements"]
                            }
                        ]
                    })
                )
            )
        )
    ]
    mock_response.usage = MagicMock(
        total_tokens=100,
        prompt_tokens=50,
        completion_tokens=50
    )
    
    # Set up the mock chain
    mock_completions.create = AsyncMock(return_value=mock_response)
    mock_chat.completions = mock_completions
    mock_client.chat = mock_chat
    
    return mock_client

@pytest.fixture
def resume_analyzer(mock_openai_client):
    """Create a ResumeAnalyzer instance with mock client."""
    return ResumeAnalyzer(openai_client=mock_openai_client)

@pytest.fixture
def sample_education_section():
    """Sample education section for testing."""
    return """
    Education:
    Stanford University
    Bachelor of Science in Computer Science, 2023
    GPA: 3.8
    Relevant Coursework: Data Structures, Algorithms, Machine Learning
    Projects: Senior Thesis on AI Ethics
    Activities: ACM Club President
    """

@pytest.mark.asyncio
async def test_education_section_analysis(resume_analyzer, sample_education_section):
    """Test analysis of a complete education section."""
    result = await resume_analyzer._analyze_education(sample_education_section)
    
    assert "type" in result
    assert result["type"] == "Education"
    assert "points" in result
    assert len(result["points"]) > 0
    
    point = result["points"][0]
    assert "school" in point
    assert "degree" in point
    assert "graduation_date" in point
    assert "gpa" in point
    assert "coursework" in point
    assert "projects" in point
    assert "activities" in point

@pytest.mark.asyncio
async def test_education_section_with_various_formats(resume_analyzer):
    """Test analysis of education sections in different formats."""
    formats = [
        """
        EDUCATION
        Stanford University | 2019-2023
        B.S. Computer Science
        """,
        """
        Education
        * Stanford University
        * Bachelor of Science in Computer Science (2023)
        """,
        """
        Academic Background
        Stanford University
        Computer Science, B.S., 2023
        """
    ]
    
    for format_text in formats:
        result = await resume_analyzer._analyze_education(format_text)
        assert "type" in result
        assert result["type"] == "Education"
        assert "points" in result
        assert len(result["points"]) > 0

@pytest.mark.asyncio
async def test_education_section_error_handling(resume_analyzer, mock_openai_client):
    """Test error handling in education section analysis."""
    # Configure mock to raise an exception
    mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
    
    # Test with empty section
    result = await resume_analyzer._analyze_education("")
    assert result["type"] == "Education"
    assert len(result["points"]) == 0
    
    # Test with malformed section
    result = await resume_analyzer._analyze_education("Invalid JSON")
    assert result["type"] == "Education"
    assert len(result["points"]) == 0

@pytest.mark.asyncio
async def test_education_section_integration(resume_analyzer, sample_education_section):
    """Test education section as part of full resume analysis."""
    result = await resume_analyzer._analyze_education(sample_education_section)
    
    assert "type" in result
    assert result["type"] == "Education"
    assert "points" in result
    assert len(result["points"]) > 0
    
    for point in result["points"]:
        assert "school" in point
        assert "degree" in point
        assert "graduation_date" in point
        assert isinstance(point["school"], str)
        assert isinstance(point["degree"], str)
        assert isinstance(point["graduation_date"], str) 