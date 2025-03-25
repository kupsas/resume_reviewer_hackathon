#!/usr/bin/env python3
"""
STAR Analysis Prompt Testing

This script tests different system prompts for STAR format analysis in resume bullet points,
ranging from very strict to very lenient. It runs parallel analyses on a resume and reports
the results for comparison.
"""

import asyncio
import json
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any
import os
import PyPDF2
from openai import AsyncOpenAI

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    logger.error("⚠️ Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

client = AsyncOpenAI(api_key=api_key)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        logger.error(f"⚠️ Error extracting text from PDF: {e}")
        sys.exit(1)

# Define different system prompts with varying strictness levels
SYSTEM_PROMPTS = {
    "very_strict": """You are an expert resume analyzer with very strict criteria for STAR format assessment.

1. For Experience and Projects sections:
   - Extract each bullet point
   - Analyze STAR format with EXTREMELY STRICT criteria:
     * Situation (S): Must explicitly describe the context with clear situational keywords like "when", "during", "while"
     * Action (A): Must detail specific steps taken with first-person action verbs like "implemented", "developed", "created"
     * Result (R): Must explicitly state outcomes with quantifiable metrics and numbers
   - Only mark STAR components as present when explicitly stated with keywords - never infer or assume
   - Identify metrics and quantifiable achievements
   - Provide detailed rationale for each STAR component assessment

2. For Education section:
   - Extract school name, degree, graduation date
   - Identify relevant coursework (if any)
   - List projects completed (if any)
   - List co-curricular activities (if any)

3. For Skills/Certifications:
   - List all technical skills
   - List all certifications with dates
   - Group skills by category (e.g., Programming Languages, Frameworks, Tools)""",

    "strict": """You are an expert resume analyzer. For each section in the resume:

1. For Experience and Projects sections:
   - Extract each bullet point
   - Analyze STAR format with STRICT criteria:
     * Situation (S): Should clearly describe the context or scenario with minimal ambiguity
     * Action (A): Should describe specific actions taken with concrete methodology
     * Result (R): Should clearly indicate the outcome with quantifiable metrics and measurable impact
   - Mark components as present only with clear evidence - minimal inference allowed
   - Identify metrics and quantifiable achievements
   - Provide rationale for each STAR component assessment

2. For Education section:
   - Extract school name, degree, graduation date
   - Identify relevant coursework (if any)
   - List projects completed (if any)
   - List co-curricular activities (if any)

3. For Skills/Certifications:
   - List all technical skills
   - List all certifications with dates
   - Group skills by category (e.g., Programming Languages, Frameworks, Tools)""",

    "balanced": """You are an expert resume analyzer. For each section in the resume:

1. For Experience and Projects sections:
   - Extract each bullet point
   - Analyze STAR format with BALANCED criteria:
     * Situation (S): Should describe the context with situational keywords
     * Action (A): Should detail steps taken with action verbs
     * Result (R): Should include measurable outcomes with metrics
   - Identify metrics and quantifiable achievements
   - Provide detailed rationale for each STAR component assessment

2. For Education section:
   - Extract school name, degree, graduation date
   - Identify relevant coursework (if any)
   - List projects completed (if any)
   - List co-curricular activities (if any)

3. For Skills/Certifications:
   - List all technical skills
   - List all certifications with dates
   - Group skills by category (e.g., Programming Languages, Frameworks, Tools)""",

    "lenient": """You are an expert resume analyzer. For each section in the resume:

1. For Experience and Projects sections:
   - Extract each bullet point
   - Analyze STAR format with LENIENT criteria:
     * Situation (S): May be implied from context
     * Action (A): Should be clear but may be high-level
     * Result (R): May be qualitative or implied
   - Identify metrics and achievements where present
   - Provide detailed rationale for each STAR component assessment

2. For Education section:
   - Extract school name, degree, graduation date
   - Identify relevant coursework (if any)
   - List projects completed (if any)
   - List co-curricular activities (if any)

3. For Skills/Certifications:
   - List all technical skills
   - List all certifications with dates
   - Group skills by category (e.g., Programming Languages, Frameworks, Tools)""",

    "very_lenient": """You are an expert resume analyzer. For each section in the resume:

1. For Experience and Projects sections:
   - Extract each bullet point
   - Analyze STAR format with VERY LENIENT criteria:
     * Situation (S): May be inferred from context
     * Action (A): May be high-level or implied
     * Result (R): May be qualitative or implied
   - Identify any metrics or achievements mentioned
   - Provide detailed rationale for each STAR component assessment

2. For Education section:
   - Extract school name, degree, graduation date
   - Identify relevant coursework (if any)
   - List projects completed (if any)
   - List co-curricular activities (if any)

3. For Skills/Certifications:
   - List all technical skills
   - List all certifications with dates
   - Group skills by category (e.g., Programming Languages, Frameworks, Tools)"""
}

# Define the function schema for resume analysis
RESUME_ANALYSIS_FUNCTION = {
    "name": "analyze_resume_with_rationale",
    "description": "Analyze resume points for STAR format with detailed rationale",
    "parameters": {
        "type": "object",
        "properties": {
            "points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The resume point text"},
                        "star": {
                            "type": "object",
                            "properties": {
                                "situation": {"type": "boolean", "description": "Whether situation is present"},
                                "situation_rationale": {"type": "string", "description": "Explanation for situation assessment"},
                                "action": {"type": "boolean", "description": "Whether action is present"},
                                "action_rationale": {"type": "string", "description": "Explanation for action assessment"},
                                "result": {"type": "boolean", "description": "Whether result is present"},
                                "result_rationale": {"type": "string", "description": "Explanation for result assessment"},
                                "complete": {"type": "boolean", "description": "Whether all STAR components are present"}
                            },
                            "required": ["situation", "situation_rationale", "action", "action_rationale", "result", "result_rationale", "complete"]
                        }
                    },
                    "required": ["text", "star"]
                }
            }
        },
        "required": ["points"]
    }
}

# Define the test points
TEST_POINTS = [
    "Own £75M ARR Portfolio: Drive the roadmap for expenses, bills, and invoicing across 4 countries, delivering revenue goals.",
    "Product & Engineering Leadership: Lead quarterly OKRs & execution, managing 3 PMs, a designer, and an analyst, with product leadership spanning 40+ engineering teams across 3 squads. Delivered a deserving promotion.",
    "Led development of cloud-based microservices architecture, improving system reliability by 99.9%",
    "Implemented CI/CD pipeline using Jenkins and Docker",
    "Created customer Analysis and Demographic reports for the Markham Economic Development website, enabling the Markham Business community to make better marketing and product placement decisions.",
    "Led the operational strategy group for implementing online & offline stakeholder connect initiatives across 14 regions, increasing engagement footfall by 15x and monetizing 3 impactful revenue models in 4 years.",
    "Increased the MAU by 4x over two quarters by optimizing key product flows in user onboarding & retention in collaboration with Growth Teams.",
    "Provided strategic insights to teams across Tide (onboarding + subscriptions + platform experience) to design roadmap + features."
]

async def analyze_resume_with_prompt(points: List[str], prompt_name: str, system_prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    """Analyze resume points using specific system prompt with retries."""
    for attempt in range(max_retries):
        try:
            logger.info(f"Running analysis with '{prompt_name}' prompt... (Attempt {attempt + 1}/{max_retries})")
            
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze the following resume points with detailed rationale for STAR components:\n\n" + "\n".join(points)}
                ],
                functions=[RESUME_ANALYSIS_FUNCTION],
                function_call={"name": "analyze_resume_with_rationale"},
                temperature=0
            )
            
            # Parse the function call response
            analysis_result = json.loads(response.choices[0].message.function_call.arguments)
            
            logger.info(f"✓ Analysis with '{prompt_name}' prompt completed")
            
            return {
                "prompt_name": prompt_name,
                "prompt_description": prompt_name.replace("_", " ").title(),
                "analysis": analysis_result
            }
        except Exception as e:
            logger.error(f"⚠️ Error analyzing resume with {prompt_name} prompt (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
            else:
                return {
                    "prompt_name": prompt_name,
                    "prompt_description": prompt_name.replace("_", " ").title(),
                    "error": str(e)
                }

async def analyze_with_all_prompts(points: List[str]) -> List[Dict[str, Any]]:
    """Run sequential analysis with all system prompts."""
    results = []
    for prompt_name, system_prompt in SYSTEM_PROMPTS.items():
        # Add 5-second delay between each analysis
        if results:  # Don't delay before the first analysis
            logger.info("⏳ Waiting 5 seconds before next analysis to avoid rate limiting...")
            await asyncio.sleep(5)
        
        result = await analyze_resume_with_prompt(points, prompt_name, system_prompt)
        results.append(result)
    
    logger.info(f"✓ Completed {len(results)} analyses")
    return results

def print_summary_table(results: List[Dict[str, Any]]):
    """Print a summary table of STAR analysis results."""
    print("\n🌟 STAR Component Summary Across Prompts 🌟")
    print("-" * 100)
    print(f"{'Prompt Type':<15} | {'Complete STAR %':<15} | {'Situation %':<15} | {'Action %':<15} | {'Result %':<15}")
    print("-" * 100)
    
    for result in results:
        if "error" in result:
            print(f"{result['prompt_name']:<15} | Error: {result['error']}")
            continue
            
        points = result["analysis"]["points"]
        total_points = len(points)
        
        # Calculate percentages
        situation_count = sum(1 for p in points if p["star"]["situation"])
        action_count = sum(1 for p in points if p["star"]["action"])
        result_count = sum(1 for p in points if p["star"]["result"])
        complete_count = sum(1 for p in points if p["star"]["complete"])
        
        situation_pct = (situation_count / total_points) * 100 if total_points > 0 else 0
        action_pct = (action_count / total_points) * 100 if total_points > 0 else 0
        result_pct = (result_count / total_points) * 100 if total_points > 0 else 0
        complete_pct = (complete_count / total_points) * 100 if total_points > 0 else 0
        
        print(f"{result['prompt_name']:<15} | {complete_pct:>6.1f}% | {situation_pct:>6.1f}% | {action_pct:>6.1f}% | {result_pct:>6.1f}%")
    
    print("-" * 100)
    print("\n📝 Detailed STAR Analysis for Sample Points 📝")
    
    # Print detailed analysis for first two points
    for result in results:
        if "error" in result:
            continue
            
        print(f"\n{result['prompt_name'].replace('_', ' ').title()} Analysis:")
        print("-" * 80)
        
        for point in result["analysis"]["points"][:2]:  # Only show first two points
            print(f"\nText: {point['text']}")
            print("-" * 80)
            
            star = point["star"]
            print(f"✅ Complete STAR: {'Yes' if star['complete'] else 'No'}")
            print(f"🔍 Situation: {'Yes' if star['situation'] else 'No'}")
            print(f"  Rationale: {star['situation_rationale']}")
            print(f"🔨 Action: {'Yes' if star['action'] else 'No'}")
            print(f"  Rationale: {star['action_rationale']}")
            print(f"🏆 Result: {'Yes' if star['result'] else 'No'}")
            print(f"  Rationale: {star['result_rationale']}")
            print("-" * 80)

def print_detailed_analysis(results: List[Dict[str, Any]]):
    """Print detailed analysis of sample points with rationales."""
    # Get a sample point that appears in all analyses
    sample_points = []
    
    if all("analysis" in result for result in results):
        # Find sections that exist in all results
        common_sections = []
        for section_type in ["Experience", "Projects"]:
            for result in results:
                sections = [s for s in result["analysis"]["sections"] if s["type"] == section_type]
                if not sections:
                    break
            else:
                common_sections.append(section_type)
        
        # For each common section, get some sample points
        for section_type in common_sections:
            for result_idx, result in enumerate(results):
                sections = [s for s in result["analysis"]["sections"] if s["type"] == section_type]
                if sections and sections[0]["points"]:
                    # Take first few points from first section of this type
                    for point_idx, point in enumerate(sections[0]["points"][:3]):
                        if result_idx == 0:  # Only add new sample points from first result
                            sample_points.append({
                                "text": point["text"],
                                "section_type": section_type,
                                "analyses": [{
                                    "prompt_name": results[0]["prompt_description"],
                                    "star": point["star"]
                                }]
                            })
                        elif point_idx < len(sample_points) and sample_points[point_idx]["text"] == point["text"]:
                            # Add this analysis to existing sample point
                            sample_points[point_idx]["analyses"].append({
                                "prompt_name": result["prompt_description"],
                                "star": point["star"]
                            })
    
    # Print detailed analysis for sample points
    if sample_points:
        print("\n📝 Detailed STAR Analysis for Sample Points 📝")
        
        for i, sample in enumerate(sample_points[:3]):  # Limit to 3 samples
            print(f"\nSample Point {i+1} ({sample['section_type']}):")
            print(f"Text: {sample['text']}")
            print("-" * 100)
            
            # Print STAR analysis from each prompt
            for analysis in sample["analyses"]:
                print(f"\n{analysis['prompt_name']} Analysis:")
                star = analysis["star"]
                print(f"✅ Complete STAR: {'Yes' if star['complete'] else 'No'}")
                print(f"🔍 Situation: {'Yes' if star['situation'] else 'No'}")
                print(f"  Rationale: {star['situation_rationale']}")
                print(f"📋 Task: {'Yes' if star['task'] else 'No'}")
                print(f"  Rationale: {star['task_rationale']}")
                print(f"🔨 Action: {'Yes' if star['action'] else 'No'}")
                print(f"  Rationale: {star['action_rationale']}")
                print(f"🏆 Result: {'Yes' if star['result'] else 'No'}")
                print(f"  Rationale: {star['result_rationale']}")
                print("-" * 50)
    else:
        print("\n⚠️ No common sample points found for detailed analysis")

def save_results_to_file(results: List[Dict[str, Any]], file_path: str):
    """Save analysis results to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Results saved to {file_path}")
    except Exception as e:
        print(f"⚠️ Error saving results: {e}")

def read_test_points(file_path: str) -> List[str]:
    """Read test points from a file."""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            # Skip the header line and strip whitespace
            points = [line.strip() for line in lines[1:] if line.strip()]
            # Remove the numbering from the points
            points = [point.split('. ', 1)[1] if '. ' in point else point for point in points]
            return points
    except Exception as e:
        logger.error(f"⚠️ Error reading test points: {e}")
        sys.exit(1)

async def main():
    """Main function to run the STAR analysis test."""
    logger.info("🚀 Starting STAR Analysis Prompt Testing")
    
    try:
        # Read test points from file
        test_points_file = "tests/data/test_points.txt"
        test_points = read_test_points(test_points_file)
        logger.info(f"📝 Read {len(test_points)} test points from {test_points_file}")
        
        # Analyze points with all prompts
        logger.info("🔍 Analyzing resume points with 5 different STAR analysis prompts...")
        results = await analyze_with_all_prompts(test_points)
        
        # Save results to JSON file
        output_file = "star_analysis_results_test_points.json"
        with open(output_file, "w") as f:
            json.dump({"results": results}, f, indent=2)
        
        logger.info(f"✅ Results saved to {output_file}")
        
        # Print summary table
        print_summary_table(results)
        
    except Exception as e:
        logger.error(f"❌ Error in main: {str(e)}")
        raise e

if __name__ == "__main__":
    asyncio.run(main())
