"""Test script for analyzing an actual resume with a job description."""
import asyncio
import json
from pathlib import Path
import PyPDF2
import requests
import time
import re
import textwrap

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

async def test_resume_analysis():
    """Test resume analysis with an actual resume and job description."""
    # File paths
    resume_path = "tests/data/resumes/Resume - Vinod Krishna .pdf"
    job_desc_path = "tests/data/job_descriptions/sample_job_Vinod_1.txt"
    
    try:
        # Start timing
        start_time = time.time()
        
        # Read resume content
        print(f"\n📄 Reading resume from: {resume_path}")
        resume_text = read_pdf_content(resume_path)
        
        # Read job description
        print(f"\n📋 Reading job description from: {job_desc_path}")
        job_description = read_text_file(job_desc_path)
        
        print("\n📝 Files loaded successfully!")
        print("\n--- First 500 characters of resume ---")
        preview_text = clean_text(resume_text[:500]) + ("..." if len(resume_text) > 500 else "")
        print(preview_text)
        
        print("\n--- First 500 characters of job description ---")
        preview_jd = clean_text(job_description[:500]) + ("..." if len(job_description) > 500 else "")
        print(preview_jd)
        
        # API endpoint
        url = "http://localhost:8000/api/resume/analyze"
        
        # Prepare the request data
        data = {
            "resume_text": resume_text,
            "job_description": job_description
        }
        
        print("\n🔍 Sending resume and job description for analysis...")
        
        # Make the request
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Parse and print the results
        result = response.json()
        
        # Print raw JSON
        print("\n📋 Raw JSON Response:")
        print(json.dumps(result, indent=2))
        
        print("\n=== Resume Analysis Results ===\n")
        
        # Print job match analysis if available
        if "jobMatchAnalysis" in result:
            job_match = result["jobMatchAnalysis"]
            print(f"\n🎯 Job Match Score: {job_match['match_score']:.1f}/100")
            
            # Print technical match
            if "technical_match" in job_match:
                tech_match = job_match["technical_match"]
                print("\n💻 Technical Skills Match:")
                print(f"  • Matched Skills: {', '.join(tech_match['matched_skills'])}")
                print(f"  • Missing Skills: {', '.join(tech_match['missing_skills'])}")
                print(f"  • Coverage Score: {tech_match['skill_coverage_score']:.1f}/100")
            
            # Print experience match
            if "experience_match" in job_match:
                exp_match = job_match["experience_match"]
                print("\n⏳ Experience Match:")
                print(f"  • Required Years: {exp_match['required_years']}")
                print(f"  • Actual Years: {exp_match['actual_years']}")
                print(f"  • Experience Score: {exp_match['experience_score']:.1f}/100")
            
            # Print key requirements
            if "key_requirements" in job_match:
                key_reqs = job_match["key_requirements"]
                print("\n✅ Key Requirements:")
                print("  • Met Requirements:")
                for req in key_reqs["met"]:
                    print(f"    - {req}")
                print("\n  • Partially Met Requirements:")
                for req in key_reqs["partially_met"]:
                    print(f"    - {req}")
                print("\n  • Not Met Requirements:")
                for req in key_reqs["not_met"]:
                    print(f"    - {req}")
            
            # Print recommendations
            if "recommendations" in job_match:
                print("\n💡 Recommendations:")
                for i, rec in enumerate(job_match["recommendations"], 1):
                    print(f"  {i}. {format_text_block(rec, width=75)}")
        
        # Print resume analysis
        if "resumeAnalysis" in result:
            analysis = result["resumeAnalysis"]
            
            # Print match score if available
            if "match_score" in analysis:
                print(f"\n🎯 Job Match Score: {analysis['match_score']:.1f}/5.0")
            
            # Print sections
            if "sections" in analysis:
                print("\n📑 Analyzed Sections:")
                for section in analysis["sections"]:
                    print(f"\n🔹 {section['type']}:")
                    if "points" in section:
                        for point in section["points"]:
                            print(f"\n  • {format_text_block(point['text'], width=75)}")
                            if "star" in point:
                                star = point["star"]
                                print(f"    STAR Format: {'✅' if star.get('complete') else '❌'}")
                                if not star.get("complete"):
                                    print("    Missing STAR components:")
                                    for component in ["situation", "task", "action", "result"]:
                                        if not star.get(component):
                                            print(f"      - {component.title()}")
                            if "metrics" in point and point["metrics"]:
                                print(f"    📊 Metrics found: {', '.join(point['metrics'])}")
                            if "technical_score" in point:
                                print(f"    💻 Technical depth: {point['technical_score']:.1f}/5.0")
            
            # Print scores
            if "scores" in analysis:
                print("\n📈 Overall Scores:")
                scores = analysis["scores"]
                print(f"  • STAR Format: {scores['star_format']:.1f}/5.0")
                print(f"  • Metrics Usage: {scores['metrics_usage']:.1f}/5.0")
                print(f"  • Technical Depth: {scores['technical_depth']:.1f}/5.0")
                print(f"  • Overall Score: {scores['overall']:.1f}/5.0")
            
            # Print job-specific recommendations if available
            if "job_specific_recommendations" in analysis:
                print("\n💼 Job-Specific Recommendations:")
                for i, rec in enumerate(analysis["job_specific_recommendations"], 1):
                    print(f"  {i}. {format_text_block(rec, width=75)}")
        
        # Print execution time
        print(f"\n⏱️ Execution Time: {execution_time:.2f} seconds")
        
        # Print token usage
        if "tokenUsage" in result:
            usage = result["tokenUsage"]
            print("\n💰 Resource Usage:")
            print(f"  • Total Tokens: {usage['total_tokens']}")
            print(f"  • Prompt Tokens: {usage['prompt_tokens']}")
            print(f"  • Completion Tokens: {usage['completion_tokens']}")
            print(f"  • Cost: ${usage['total_cost']:.4f}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print("\nError response:")
            print(json.dumps(e.response.json(), indent=2))

if __name__ == "__main__":
    print("\n🚀 Testing resume analysis with actual resume and job description...")
    asyncio.run(test_resume_analysis()) 