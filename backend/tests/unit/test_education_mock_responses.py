import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.openai_service import OpenAIService
import json

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI response."""
    return {
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
    }

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
def mock_openai_service(mock_openai_client):
    """Create a mock OpenAI service."""
    return OpenAIService(client=mock_openai_client)

@pytest.fixture
def resume_analyzer(mock_openai_client):
    """Create a ResumeAnalyzer instance with mock client."""
    return ResumeAnalyzer(openai_client=mock_openai_client)

@pytest.mark.asyncio
async def test_education_analysis_with_mock(resume_analyzer, mock_openai_response):
    """Test education analysis with mock response."""
    sample_text = """
    Education:
    Stanford University
    Bachelor of Science in Computer Science, 2023
    GPA: 3.8
    Relevant Coursework: Data Structures, Algorithms, Machine Learning
    Projects: Senior Thesis on AI Ethics
    Activities: ACM Club President
    """
    
    result = await resume_analyzer._analyze_education(sample_text)
    assert "type" in result
    assert result["type"] == "Education"
    assert "points" in result
    assert len(result["points"]) == len(mock_openai_response["sections"][0]["points"])

@pytest.mark.asyncio
async def test_education_analysis_error_handling(resume_analyzer, mock_openai_client):
    """Test error handling in education analysis."""
    mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
    
    result = await resume_analyzer._analyze_education("Sample text")
    assert "type" in result
    assert result["type"] == "Education"
    assert "points" in result
    assert len(result["points"]) == 0

@pytest.mark.asyncio
async def test_education_analysis_validation(resume_analyzer, mock_openai_client):
    """Test validation of education analysis response."""
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                function_call=MagicMock(
                    arguments=json.dumps({
                        "sections": [
                            {
                                "type": "Education",
                                "points": [],
                                "reputation_score": 0,
                                "suggestions": []
                            }
                        ]
                    })
                )
            )
        )
    ]
    mock_response.usage = MagicMock(
        total_tokens=50,
        prompt_tokens=25,
        completion_tokens=25
    )
    mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    result = await resume_analyzer._analyze_education("Invalid education text")
    assert "type" in result
    assert result["type"] == "Education"
    assert "points" in result
    assert len(result["points"]) == 0

@pytest.mark.asyncio
async def test_education_analysis_rate_limiting(resume_analyzer, mock_openai_client):
    """Test rate limiting handling in education analysis."""
    # Configure mock to raise rate limit error first, then succeed on retry
    mock_response = MagicMock(
        choices=[
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
        ],
        usage=MagicMock(
            total_tokens=100,
            prompt_tokens=50,
            completion_tokens=50
        )
    )
    
    # Set up side effects for the create method
    mock_openai_client.chat.completions.create.side_effect = [
        Exception("Rate limit exceeded"),  # First call fails
        mock_response  # Second call succeeds
    ]
    
    result = await resume_analyzer._analyze_education("Sample education text")
    assert result["type"] == "Education"
    assert len(result["points"]) > 0
    assert result["points"][0]["school"] == "Stanford University"
    
    # Verify that the create method was called twice (initial + retry)
    assert mock_openai_client.chat.completions.create.call_count == 2 