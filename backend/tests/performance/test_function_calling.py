"""Performance tests for function calling implementation."""
import pytest
import asyncio
import time
from pathlib import Path
import PyPDF2
import json
from app.services.openai_service import OpenAIService, RESUME_ANALYSIS_FUNCTIONS, JOB_MATCH_FUNCTIONS
from app.core.config import settings

async def run_performance_test():
    """Run a detailed performance test with real resume and job description data."""
    openai_service = OpenAIService()
    
    # Read test data
    test_data_dir = Path(__file__).parent.parent / "data"
    resume_path = test_data_dir / "resumes" / "Sashank_Resume.pdf"
    job_desc_path = test_data_dir / "job_descriptions" / "sample_job.txt"
    
    # Read PDF file
    with open(resume_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    
    # Read job description
    with open(job_desc_path, "r") as f:
        job_description = f.read()
    
    print("\n📊 PERFORMANCE TEST RESULTS")
    print("="*80)
    
    # Test 1: Resume Analysis Only
    print("\n🔍 Resume Analysis Performance:")
    print("-"*50)
    
    start_time = time.time()
    resume_response = await openai_service.client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": """You are an expert resume analyzer. For each section in the resume:

1. For Experience and Projects sections:
   - Extract each bullet point
   - Analyze STAR format (Situation, Task, Action, Result)
   - Identify metrics and quantifiable achievements
   - Provide a one-sentence suggestion for improvement following STAR format with metrics

2. For Education section:
   - Extract school name, degree, graduation date
   - Identify relevant coursework (if any)
   - List projects completed (if any)
   - List co-curricular activities (if any)

3. For Skills/Certifications:
   - List all technical skills
   - List all certifications with dates
   - Group skills by category (e.g., Programming Languages, Frameworks, Tools)"""
            },
            {"role": "user", "content": resume_text}
        ],
        functions=RESUME_ANALYSIS_FUNCTIONS,
        function_call={"name": "analyze_resume_section"},
        temperature=0
    )
    resume_time = time.time() - start_time
    
    # Calculate resume analysis costs
    resume_tokens = {
        "total": resume_response.usage.total_tokens,
        "prompt": resume_response.usage.prompt_tokens,
        "completion": resume_response.usage.completion_tokens
    }
    resume_cost = (
        resume_tokens["prompt"] * settings.COST_PER_INPUT_TOKEN +
        resume_tokens["completion"] * settings.COST_PER_OUTPUT_TOKEN
    )
    
    print(f"Total Time: {resume_time:.2f} seconds")
    print(f"Token Usage:")
    print(f"  - Prompt Tokens: {resume_tokens['prompt']}")
    print(f"  - Completion Tokens: {resume_tokens['completion']}")
    print(f"  - Total Tokens: {resume_tokens['total']}")
    print(f"Cost: ${resume_cost:.4f}")
    
    print("\n📄 Raw Function Call:")
    print(resume_response.choices[0].message.function_call)
    print("\n📄 Raw Arguments:")
    print(resume_response.choices[0].message.function_call.arguments)
    
    # Test 2: Job Match Analysis
    print("\n🎯 Job Match Analysis Performance:")
    print("-"*50)
    
    start_time = time.time()
    job_response = await openai_service.client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": """You are an expert at matching resumes to job descriptions.
For each section in the resume:

1. For Experience and Projects sections:
   - Analyze each point's relevance to the job
   - Provide a one-sentence suggestion to better align with job requirements
   - Follow STAR format and include metrics where possible

2. For Education section:
   - Analyze how coursework aligns with job requirements
   - Provide one-sentence recommendation on how to better present education, coursework, projects, and co-curriculars to match the job

3. For Skills/Certifications section:
   - Provide one-sentence recommendation on how to better present skills and certifications to match the job"""
            },
            {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"}
        ],
        functions=JOB_MATCH_FUNCTIONS,
        function_call={"name": "analyze_job_match"},
        temperature=0
    )
    job_time = time.time() - start_time
    
    # Calculate job match costs
    job_tokens = {
        "total": job_response.usage.total_tokens,
        "prompt": job_response.usage.prompt_tokens,
        "completion": job_response.usage.completion_tokens
    }
    job_cost = (
        job_tokens["prompt"] * settings.COST_PER_INPUT_TOKEN +
        job_tokens["completion"] * settings.COST_PER_OUTPUT_TOKEN
    )
    
    print(f"Total Time: {job_time:.2f} seconds")
    print(f"Token Usage:")
    print(f"  - Prompt Tokens: {job_tokens['prompt']}")
    print(f"  - Completion Tokens: {job_tokens['completion']}")
    print(f"  - Total Tokens: {job_tokens['total']}")
    print(f"Cost: ${job_cost:.4f}")
    
    print("\n📄 Raw Function Call:")
    print(job_response.choices[0].message.function_call)
    print("\n📄 Raw Arguments:")
    print(job_response.choices[0].message.function_call.arguments)
    
    # Overall Performance Summary
    print("\n📈 Overall Performance Summary:")
    print("="*80)
    print(f"Total Execution Time: {resume_time + job_time:.2f} seconds")
    print(f"Total Tokens Used: {resume_tokens['total'] + job_tokens['total']}")
    print(f"Total Cost: ${resume_cost + job_cost:.4f}")
    
    return {
        "resume": {
            "time": resume_time,
            "tokens": resume_tokens,
            "cost": resume_cost,
            "output": json.loads(resume_response.choices[0].message.function_call.arguments)
        },
        "job": {
            "time": job_time,
            "tokens": job_tokens,
            "cost": job_cost,
            "output": json.loads(job_response.choices[0].message.function_call.arguments)
        },
        "total": {
            "time": resume_time + job_time,
            "tokens": resume_tokens["total"] + job_tokens["total"],
            "cost": resume_cost + job_cost
        }
    }

@pytest.mark.asyncio
async def test_function_calling_performance():
    """Test the performance of function calling implementation with real data."""
    print("\n=== Function Calling Performance Test (Using Real Data) ===\n")
    
    result = await run_performance_test()
    
    # Basic assertions to ensure quality
    assert result["resume"]["output"] is not None, "Resume analysis failed"
    assert result["job"]["output"] is not None, "Job match analysis failed"
    assert result["resume"]["time"] > 0, "Invalid resume analysis time"
    assert result["job"]["time"] > 0, "Invalid job match time"
    assert result["total"]["time"] > 0, "Invalid total execution time"
    assert result["total"]["tokens"] > 0, "No tokens used"
    assert result["total"]["cost"] > 0, "No cost calculated" 