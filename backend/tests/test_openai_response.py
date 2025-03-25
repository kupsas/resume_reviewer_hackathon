"""Test script to check raw OpenAI API responses for resume analysis and job matching."""
import asyncio
import json
from pathlib import Path
import logging
import sys
import os
import httpx
import PyPDF2

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

from app.services.openai_service import OpenAIService
from app.core.config import settings
from openai import AsyncOpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_pdf_content(file_path: str) -> str:
    """Read content from a PDF file."""
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text

async def test_openai_responses():
    """Test raw OpenAI API responses for resume analysis and job matching."""
    try:
        # Initialize OpenAI service with correct client configuration
        client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            http_client=httpx.AsyncClient(
                timeout=60.0,
                follow_redirects=True
            )
        )
        openai_service = OpenAIService(client)
        
        # Read test files
        resume_path = "tests/data/resumes/Resume - Vinod Krishna .pdf"
        job_desc_path = "tests/data/job_descriptions/sample_job_Vinod_1.txt"
        
        # Read resume content
        print("\n📄 Reading resume from PDF...")
        resume_text = read_pdf_content(resume_path)
        print(f"  • Extracted {len(resume_text)} characters from resume")
            
        # Read job description
        with open(job_desc_path, 'r') as file:
            job_description = file.read()
        print(f"  • Read {len(job_description)} characters from job description")
        
        print("\n🚀 Testing Raw OpenAI API Responses...")
        print("Note: This test bypasses our backend API and tests OpenAI responses directly")
        print("-" * 50)
        
        # Test 1: Resume Analysis
        print("\n📄 Testing OpenAI Resume Analysis...")
        print("-" * 50)
        
        resume_response = await openai_service.analyze_resume_content(resume_text)
        
        print("\n📋 Raw OpenAI Resume Analysis Response:")
        print("Function Call Arguments:")
        print(json.dumps(resume_response, indent=2))
        
        # Test 2: Job Match Analysis
        print("\n🎯 Testing OpenAI Job Match Analysis...")
        print("-" * 50)
        
        job_match_response = await openai_service.analyze_job_match(resume_text, job_description)
        
        print("\n📋 Raw OpenAI Job Match Analysis Response:")
        print("Function Call Arguments:")
        print(json.dumps(job_match_response, indent=2))
        
        # Validate responses
        print("\n🔍 OpenAI Response Validation:")
        print("-" * 50)
        
        # Check resume analysis
        if resume_response["status"] == "success":
            print("✅ OpenAI Resume Analysis: Success")
            print(f"  • Token Usage: {resume_response['token_usage']['total_tokens']} tokens")
            print(f"  • Cost: ${resume_response['token_usage']['total_cost']:.4f}")
            
            # Log the raw function call arguments
            print("\n📝 Raw Function Call Arguments:")
            print(json.dumps(resume_response["content"], indent=2))
        else:
            print("❌ OpenAI Resume Analysis: Failed")
            print(f"  • Error: {resume_response.get('message', 'Unknown error')}")
        
        # Check job match analysis
        if job_match_response["status"] == "success":
            print("\n✅ OpenAI Job Match Analysis: Success")
            print(f"  • Token Usage: {job_match_response['token_usage']['total_tokens']} tokens")
            print(f"  • Cost: ${job_match_response['token_usage']['total_cost']:.4f}")
            
            # Log the raw function call arguments
            print("\n📝 Raw Function Call Arguments:")
            print(json.dumps(job_match_response["content"], indent=2))
            
            # Validate job match structure
            content = job_match_response["content"]
            required_fields = ["match_score", "technical_match", "experience_match", "key_requirements", "recommendations"]
            
            print("\n📊 Job Match Structure Validation:")
            for field in required_fields:
                if field in content:
                    print(f"  • {field}: ✅ Present")
                    if field == "technical_match":
                        tech_match = content[field]
                        print(f"    - matched_skills: {len(tech_match.get('matched_skills', []))} items")
                        print(f"    - missing_skills: {len(tech_match.get('missing_skills', []))} items")
                        print(f"    - skill_coverage_score: {tech_match.get('skill_coverage_score', 0)}")
                    elif field == "experience_match":
                        exp_match = content[field]
                        print(f"    - required_years: {exp_match.get('required_years', 0)}")
                        print(f"    - actual_years: {exp_match.get('actual_years', 0)}")
                        print(f"    - experience_score: {exp_match.get('experience_score', 0)}")
                    elif field == "key_requirements":
                        key_reqs = content[field]
                        print(f"    - met: {len(key_reqs.get('met', []))} items")
                        print(f"    - partially_met: {len(key_reqs.get('partially_met', []))} items")
                        print(f"    - not_met: {len(key_reqs.get('not_met', []))} items")
                    elif field == "recommendations":
                        print(f"    - count: {len(content.get('recommendations', []))} items")
                else:
                    print(f"  • {field}: ❌ Missing")
        else:
            print("\n❌ OpenAI Job Match Analysis: Failed")
            print(f"  • Error: {job_match_response.get('message', 'Unknown error')}")
        
        # Clean up
        await client.close()
        
    except Exception as e:
        logger.error(f"Error in test: {str(e)}", exc_info=True)
        print(f"\n❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 Starting Raw OpenAI Response Tests...")
    asyncio.run(test_openai_responses()) 