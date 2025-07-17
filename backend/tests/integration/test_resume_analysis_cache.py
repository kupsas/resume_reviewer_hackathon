import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_resume_analyzer
from app.services.resume_analyzer import ResumeAnalyzer

@pytest.mark.asyncio
async def test_resume_analysis_cache():
    """
    Integration test for resume analysis cache:
    - First call: cache miss (OpenAI called)
    - Second call: cache hit (OpenAI not called)
    - Third call: cache hit for resume analysis, job match is fresh
    """
    # Create a single ResumeAnalyzer instance that will be shared across all requests
    shared_analyzer = ResumeAnalyzer()
    
    # Override the dependency to use our shared instance
    app.dependency_overrides[get_resume_analyzer] = lambda: shared_analyzer
    
    try:
        client = TestClient(app)
        resume_text = "This is a test resume for cache integration."
        job_description = "This is a test job description."
        
        # Create a mock response that looks like an OpenAI response
        mock_openai_response = MagicMock()
        mock_openai_response.choices = [MagicMock()]
        mock_openai_response.choices[0].message.function_call.arguments = '{"sections": ["FAKE_SECTION"]}'
        mock_openai_response.usage.total_tokens = 100
        mock_openai_response.usage.prompt_tokens = 50
        mock_openai_response.usage.completion_tokens = 50

        # Mock the actual OpenAI API call inside the OpenAIService
        with patch.object(shared_analyzer.openai_service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_openai_call:
            mock_openai_call.return_value = mock_openai_response

            # First call: should be a cache miss (OpenAI called)
            print("Making first API call (expecting cache miss)...")
            response1 = client.post("/api/resume/analyze", json={"resume_text": resume_text})
            assert response1.status_code == 200
            assert mock_openai_call.call_count == 1
            print(f"✅ First call: OpenAI called {mock_openai_call.call_count} time(s)")

            # Second call: should be a cache hit (OpenAI not called again)
            print("Making second API call (expecting cache hit)...")
            response2 = client.post("/api/resume/analyze", json={"resume_text": resume_text})
            assert response2.status_code == 200
            assert mock_openai_call.call_count == 1  # Still only called once
            print(f"✅ Second call: OpenAI still called {mock_openai_call.call_count} time(s) (cache hit!)")

            # Third call: same resume + job description (resume analysis from cache, job match is fresh)
            print("Making third API call with job description (expecting cache hit for resume, fresh job match)...")
            response3 = client.post("/api/resume/analyze", json={"resume_text": resume_text, "job_description": job_description})
            assert response3.status_code == 200
            # The resume analysis should still be cached (1 call), but job match will make another call (2 total)
            assert mock_openai_call.call_count == 2  # One for resume analysis (cached), one for job match (fresh)
            print(f"✅ Third call: OpenAI called {mock_openai_call.call_count} time(s) total (resume cached, job match fresh)")

        print("\n🎉 All cache tests passed! Cache is working correctly.")
        
    finally:
        # Clean up the dependency override
        app.dependency_overrides.clear()

if __name__ == "__main__":
    pytest.main([__file__]) 