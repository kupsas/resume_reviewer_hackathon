"""
Test script to validate cache behavior with three different scenarios:
1. Resume only (first time) - should set cache
2. Resume only (second time) - should hit cache for instant response
3. Resume + job description - should use cached resume analysis but call OpenAI for job match
"""
import asyncio
import json
from pathlib import Path
import PyPDF2
import requests
import time
import re
import textwrap

# Get the absolute path to the backend directory
BACKEND_DIR = Path(__file__).parent.absolute()

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and normalizing line breaks."""
    # Replace multiple spaces and newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return text.strip()

def format_text_block(text: str, width: int = 80) -> str:
    """Format a text block with proper wrapping."""
    return textwrap.fill(text, width=width, break_long_words=False, break_on_hyphens=False)

def read_pdf_content(file_path: str) -> str:
    """Read content from a PDF file."""
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return clean_text(text)

def read_text_file(file_path: str) -> str:
    """Read content from a text file."""
    with open(file_path, 'r') as file:
        return clean_text(file.read())

async def run_analysis(scenario_name: str, resume_text: str, job_description: str = None):
    """Run a single analysis scenario."""
    print(f"\n{'='*60}")
    print(f"🧪 SCENARIO: {scenario_name}")
    print(f"{'='*60}")
    
    # Start timing
    start_time = time.time()
    
    # API endpoint
    url = "http://localhost:8000/api/resume/analyze"
    
    # Prepare the request data
    data = {
        "resume_text": resume_text
    }
    
    # Add job description only if provided
    if job_description:
        data["job_description"] = job_description
        print("📋 Sending resume + job description for analysis...")
    else:
        print("📄 Sending resume only for analysis...")
    
    try:
        # Make the request
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Parse the results
        result = response.json()
        
        # Print summary information
        print(f"\n✅ Analysis completed successfully!")
        print(f"⏱️  Execution Time: {execution_time:.2f} seconds")
        
        # Print cache-related information from logs (if visible)
        if execution_time < 1.0:
            print("🚀 FAST RESPONSE - Likely cache hit!")
        else:
            print("🐌 SLOWER RESPONSE - Likely cache miss or OpenAI call")
        
        # Print basic result structure
        print(f"\n📊 Response Structure:")
        if "resumeAnalysis" in result:
            print("  ✅ Resume Analysis present")
            if "scores" in result["resumeAnalysis"]:
                scores = result["resumeAnalysis"]["scores"]
                if 'overall' in scores:
                    print(f"     Overall Score: {scores['overall']:.1f}/5.0")
        
        if "jobMatchAnalysis" in result:
            print("  ✅ Job Match Analysis present")
            if result['jobMatchAnalysis'] and 'match_score' in result['jobMatchAnalysis']:
                print(f"     Match Score: {result['jobMatchAnalysis']['match_score']:.1f}/100")
        else:
            print("  ❌ No Job Match Analysis (expected for resume-only requests)")
        
        # Print token usage
        if "tokenUsage" in result:
            usage = result["tokenUsage"]
            print(f"\n💰 Token Usage:")
            print(f"  • Total Tokens: {usage['total_tokens']}")
            print(f"  • Cost: ${usage['total_cost']:.4f}")
        
        return result, execution_time
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print("\nError response:")
            try:
                print(json.dumps(e.response.json(), indent=2))
            except:
                print(e.response.text)
        return None, 0

async def main():
    """Run all three cache validation scenarios."""
    print("🚀 Starting Cache Validation Test")
    print("=" * 60)
    
    # File paths - using absolute paths from backend directory
    resume_path = BACKEND_DIR / "tests" / "data" / "resumes" / "sample_resume.pdf"
    job_desc_path = BACKEND_DIR / "tests" / "data" / "job_descriptions" / "sample_job.txt"
    
    try:
        # Read resume content
        print(f"📄 Reading resume from: {resume_path}")
        resume_text = read_pdf_content(str(resume_path))
        
        # Read job description
        print(f"📋 Reading job description from: {job_desc_path}")
        job_description = read_text_file(str(job_desc_path))
        
        print("📝 Files loaded successfully!")
        
        # Store results for comparison
        results = []
        
        # SCENARIO 1: Resume only (first time) - should set cache
        result1, time1 = await run_analysis(
            "Resume Only (First Time - Cache Miss Expected)",
            resume_text
        )
        results.append(("Resume Only #1", result1, time1))
        
        # Small delay to ensure any async operations complete
        await asyncio.sleep(1)
        
        # SCENARIO 2: Resume only (second time) - should hit cache
        result2, time2 = await run_analysis(
            "Resume Only (Second Time - Cache Hit Expected)",
            resume_text
        )
        results.append(("Resume Only #2", result2, time2))
        
        # Small delay
        await asyncio.sleep(1)
        
        # SCENARIO 3: Resume + job description - should use cached resume but call OpenAI for job match
        result3, time3 = await run_analysis(
            "Resume + Job Description (Partial Cache Hit Expected)",
            resume_text,
            job_description
        )
        results.append(("Resume + Job", result3, time3))
        
        # Print summary comparison
        print(f"\n{'='*60}")
        print("📈 CACHE VALIDATION SUMMARY")
        print(f"{'='*60}")
        
        for i, (name, result, exec_time) in enumerate(results, 1):
            if result:
                print(f"\n{i}. {name}:")
                print(f"   ⏱️  Time: {exec_time:.2f}s")
                print(f"   🎯 Cache Status: {'HIT (Fast)' if exec_time < 1.0 else 'MISS (Slow)'}")
                
                if "tokenUsage" in result:
                    usage = result["tokenUsage"]
                    print(f"   💰 Tokens: {usage['total_tokens']} (${usage['total_cost']:.4f})")
        
        # Validate expected behavior
        print(f"\n🔍 VALIDATION RESULTS:")
        
        if len(results) >= 2 and results[0][1] and results[1][1]:
            time_diff = results[1][2] - results[0][2]
            if results[1][2] < results[0][2] * 0.5:  # Second call should be much faster
                print("✅ Cache working: Second resume-only call was significantly faster")
            else:
                print("❌ Cache issue: Second resume-only call was not significantly faster")
        
        if len(results) >= 3 and results[2][1]:
            if "jobMatchAnalysis" in results[2][1]:
                print("✅ Job match analysis present in third call")
            else:
                print("❌ Job match analysis missing in third call")
        
        print(f"\n💡 Expected behavior:")
        print("   1. First call: Cache MISS - slower response, sets cache")
        print("   2. Second call: Cache HIT - fast response, uses cached resume analysis")
        print("   3. Third call: Partial cache - fast resume analysis (cached) + new job match analysis")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {str(e)}")
        print("Make sure the test data files exist in backend/tests/data/")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Cache Validation Test Script")
    print("Testing cache behavior with three scenarios...")
    asyncio.run(main()) 