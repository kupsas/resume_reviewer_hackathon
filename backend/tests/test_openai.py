import pytest
import os
from dotenv import load_dotenv
import openai
from typing import List, Dict

load_dotenv()

def test_openai_api_key():
    """Test that OpenAI API key is configured and working."""
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OpenAI API key not found in environment variables"
    
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=10
        )
        assert response is not None
        assert response.choices[0].message.content is not None
    except Exception as e:
        pytest.fail(f"OpenAI API call failed: {str(e)}")

def extract_score_from_section(response: str, section_name: str) -> str:
    """Helper function to extract score from a section, handling both single-line and multi-line formats."""
    try:
        if section_name not in response:
            return ""
        
        # Get the section content up to the next section
        section_content = response.split(section_name)[1].split("\n\n")[0]
        lines = section_content.split("\n")
        
        # Try each line until we find a number
        for line in lines:
            # Clean the line and extract digits
            cleaned = ''.join(filter(str.isdigit, line.strip()))
            if cleaned:
                return cleaned
        return ""
    except Exception as e:
        print(f"Error extracting score from section {section_name}: {str(e)}")
        return ""

def extract_category_scores(response: str, section_name: str) -> Dict[str, str]:
    """Helper function to extract and validate category scores from a specific section."""
    try:
        if section_name not in response:
            return {}
        
        scores = {}
        # Get the section content up to the next section
        section = response.split(section_name)[1].split("\n\n")[0]
        for line in section.split('\n'):
            if ':' in line:
                category, score = line.rsplit(':', 1)
                cleaned_score = ''.join(filter(str.isdigit, score.strip()))
                if cleaned_score:  # Only add if we found a valid score
                    scores[category.strip()] = cleaned_score
        return scores
    except Exception as e:
        print(f"Error extracting scores from section {section_name}: {str(e)}")
        return {}

def print_response_analysis(response: str, has_job_description: bool):
    """Helper function to print a detailed analysis of a single response."""
    print("\n")
    print("-"*100)
    print(f"Analysis for {'Job Description' if has_job_description else 'No Job Description'} Case")
    print("-"*100)
    
    print("\n📝 Raw Response:")
    print("="*80)
    print(response)
    print("="*80)
    
    # Print resume strength scores
    overall_strength = extract_score_from_section(response, "RESUME STRENGTH SCORE")
    print(f"\n💪 Overall Resume Strength: {overall_strength}")
    
    strength_scores = extract_category_scores(response, "RESUME STRENGTH CATEGORIES")
    if strength_scores:
        print("\n📊 Resume Strength Categories:")
        for category, score in strength_scores.items():
            print(f"  • {category}: {score}")
    
    # Print job match scores if applicable
    if has_job_description:
        job_match = extract_score_from_section(response, "JOB MATCH SCORE")
        print(f"\n🎯 Job Match Score: {job_match}")
        
        match_scores = extract_category_scores(response, "JOB MATCH CATEGORIES")
        if match_scores:
            print("\n📊 Job Match Categories:")
            for category, score in match_scores.items():
                print(f"  • {category}: {score}")

def get_test_prompt(has_job_description: bool) -> str:
    """Generate the appropriate test prompt based on whether there's a job description."""
    base_resume = """Resume:
John Doe
Software Engineer
5 years experience in Python
Bachelor's in Computer Science
"""

    job_description = """Job Description:
Senior Software Engineer
- 5+ years of Python development
- Experience with cloud platforms
- Strong communication skills
- Bachelor's degree required
""" if has_job_description else ""

    base_format = """
1. RESUME STRENGTH SCORE (0-100):
[number]

2. RESUME STRENGTH CATEGORIES:
Technical Skills: [number]
Experience Quality: [number]
Education: [number]
Resume Format: [number]
Overall Presentation: [number]

3. KEY STRENGTHS:
- [Strength 1]
- [Strength 2]

4. AREAS FOR IMPROVEMENT:
- [Area 1]
- [Area 2]
"""

    job_match_format = """
5. JOB MATCH SCORE (0-100):
[number]

6. JOB MATCH CATEGORIES:
Skills Match: [number]
Experience Match: [number]
Education Match: [number]
Requirements Match: [number]
Overall Fit: [number]

7. JOB-SPECIFIC RECOMMENDATIONS:
- [Recommendation 1]
- [Recommendation 2]
""" if has_job_description else ""

    return f"""Analyze this {'resume against the job description' if has_job_description else 'resume'} and provide feedback in a structured format:

{base_resume}
{job_description}
Provide your analysis in exactly this format (do not deviate):
{base_format}{job_match_format}"""

def validate_response_format(response: str, has_job_description: bool, response_number: int):
    """Validate the format of a single response."""
    try:
        print(f"\nValidating Response {response_number} Format...")
        
        # 1. Check required sections exist
        required_sections = [
            "RESUME STRENGTH SCORE",
            "RESUME STRENGTH CATEGORIES",
            "KEY STRENGTHS",
            "AREAS FOR IMPROVEMENT"
        ]
        if has_job_description:
            required_sections.extend([
                "JOB MATCH SCORE",
                "JOB MATCH CATEGORIES",
                "JOB-SPECIFIC RECOMMENDATIONS"
            ])
        
        for section in required_sections:
            assert section in response, f"Response {response_number} missing section: {section}"
        print("✅ All required sections present")
        
        # 2. Validate resume strength score format
        strength_score = extract_score_from_section(response, "RESUME STRENGTH SCORE")
        assert strength_score != "", f"Response {response_number} resume strength score not found"
        assert strength_score.isdigit(), f"Response {response_number} has invalid resume strength score format: {strength_score}"
        assert 0 <= int(strength_score) <= 100, f"Response {response_number} resume strength score out of range: {strength_score}"
        print("✅ Resume strength score format valid")
        
        # 3. Validate resume strength categories format
        strength_categories = extract_category_scores(response, "RESUME STRENGTH CATEGORIES")
        expected_strength_categories = [
            "Technical Skills",
            "Experience Quality",
            "Education",
            "Resume Format",
            "Overall Presentation"
        ]
        
        assert len(strength_categories) > 0, f"Response {response_number} has no resume strength categories"
        print("\nValidating resume strength category formats:")
        for category in expected_strength_categories:
            assert category in strength_categories, f"Response {response_number} missing strength category: {category}"
            score = strength_categories[category]
            assert score != "", f"Response {response_number} has empty score for strength category {category}"
            assert score.isdigit(), f"Response {response_number} has invalid score format for strength category {category}: {score}"
            assert 0 <= int(score) <= 100, f"Response {response_number} strength category score out of range for {category}: {score}"
            print(f"  ✅ {category}: format valid")
        
        # 4. If job description present, validate job match sections
        if has_job_description:
            # Validate job match score
            match_score = extract_score_from_section(response, "JOB MATCH SCORE")
            assert match_score != "", f"Response {response_number} job match score not found"
            assert match_score.isdigit(), f"Response {response_number} has invalid job match score format: {match_score}"
            assert 0 <= int(match_score) <= 100, f"Response {response_number} job match score out of range: {match_score}"
            print("✅ Job match score format valid")
            
            # Validate job match categories
            match_categories = extract_category_scores(response, "JOB MATCH CATEGORIES")
            expected_match_categories = [
                "Skills Match",
                "Experience Match",
                "Education Match",
                "Requirements Match",
                "Overall Fit"
            ]
            
            assert len(match_categories) > 0, f"Response {response_number} has no job match categories"
            print("\nValidating job match category formats:")
            for category in expected_match_categories:
                assert category in match_categories, f"Response {response_number} missing match category: {category}"
                score = match_categories[category]
                assert score != "", f"Response {response_number} has empty score for match category {category}"
                assert score.isdigit(), f"Response {response_number} has invalid score format for match category {category}: {score}"
                assert 0 <= int(score) <= 100, f"Response {response_number} match category score out of range for {category}: {score}"
                print(f"  ✅ {category}: format valid")
        
        # 5. Check for bullet points in list sections
        sections_with_bullets = ["KEY STRENGTHS", "AREAS FOR IMPROVEMENT"]
        if has_job_description:
            sections_with_bullets.append("JOB-SPECIFIC RECOMMENDATIONS")
        
        for section in sections_with_bullets:
            section_content = response.split(section + ":")[1].split("\n\n")[0]
            assert "- " in section_content, f"Response {response_number} {section} missing bullet points"
        print("✅ Bullet points format valid")
        
        print(f"\n✅ Response {response_number} format validation complete!")
        
    except Exception as e:
        print(f"\n❌ Format validation failed for response {response_number}:")
        print(f"Error: {str(e)}")
        print("\nFull response:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        raise e

def test_openai_response_format(capsys):
    """Test that OpenAI responses maintain consistent format for both with and without job description cases."""
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OpenAI API key not found in environment variables"
    
    client = openai.OpenAI(api_key=api_key)
    
    # Test both cases
    for has_job_description in [False, True]:
        with capsys.disabled():
            print("\n")
            print("="*100)
            print(f"Testing {'With' if has_job_description else 'Without'} Job Description Case")
            print("="*100)
            
            # Make 3 calls for each case
            responses = []
            for i in range(3):
                try:
                    print(f"\nMaking API call {i+1}/3...")
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system", 
                                "content": """You are an expert resume reviewer. Follow these rules strictly:
1. Always use the exact format specified in the prompt
2. Return scores as plain numbers only (no text, no '/100', no symbols)
3. Never add explanatory text to scores
4. Never skip any sections
5. Keep responses concise and to the point"""
                            },
                            {"role": "user", "content": get_test_prompt(has_job_description)}
                        ],
                        temperature=0.0,  # Do not change the temperature from 0.0
                        max_tokens=1000,
                        presence_penalty=0.0,
                        frequency_penalty=0.0
                    )
                    responses.append(response.choices[0].message.content)
                    print("✅ API call successful")
                except Exception as e:
                    print(f"❌ API call failed: {str(e)}")
                    pytest.fail(f"OpenAI API call failed: {str(e)}")
            
            # Analyze and validate each response
            for i, response in enumerate(responses, 1):
                print_response_analysis(response, has_job_description)
                validate_response_format(response, has_job_description, i)
            
            print(f"\n✅ All format validations passed for {'job description' if has_job_description else 'no job description'} case!")