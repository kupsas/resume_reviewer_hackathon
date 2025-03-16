import os
import pytest
from app.services.resume_analyzer import ResumeAnalyzer

def print_analysis_results(result: dict, scenario: str):
    """Helper function to print analysis results in a readable format"""
    print(f"\n{'='*80}")
    print(f"TEST SCENARIO: {scenario}")
    print(f"{'='*80}\n")
    
    if result['status'] == 'success':
        # Print raw LLM output first
        print("RAW LLM OUTPUT:")
        print(f"{'='*40}")
        print(result['analysis'])
        print(f"{'='*40}\n")
        
        # Now print parsed and formatted output
        print("FORMATTED OUTPUT:")
        print(f"{'='*40}")
        
        # Extract and print scores
        analysis = result['analysis']
        
        # Get Resume Strength Score
        if "RESUME STRENGTH SCORE" in analysis:
            score_line = [line for line in analysis.split('\n') if "RESUME STRENGTH SCORE" in line][0]
            try:
                score = int(score_line.split('\n')[0].split(':')[1].strip())
                print(f"RESUME STRENGTH SCORE: {score}")
            except (IndexError, ValueError):
                print("Error parsing Resume Strength Score")
        
        # Print the rest of the analysis
        print(analysis)
        
        # Get Job Match Score if it exists
        if "JOB MATCH SCORE" in analysis:
            score_line = [line for line in analysis.split('\n') if "JOB MATCH SCORE" in line][0]
            try:
                score = int(score_line.split('\n')[0].split(':')[1].strip())
                print(f"JOB MATCH SCORE: {score}")
            except (IndexError, ValueError):
                print("Error parsing Job Match Score")
    else:
        print(f"Error: {result['message']}")
    
    print(f"\n{'='*80}\n")

def test_new_format():
    """Test the new format with both scenarios"""
    analyzer = ResumeAnalyzer()
    
    # Test Case 1: Without Job Description
    with open('tests/data/resumes/sample_resume.txt', 'r') as file:
        resume_text = file.read()
    
    result = analyzer.analyze_resume(resume_text)
    print_analysis_results(result, "Resume Analysis Without Job Description")
    assert result['status'] == 'success'
    
    # Test Case 2: With Job Description
    with open('tests/data/job_descriptions/sample_job.txt', 'r') as file:
        job_description = file.read()
    
    result = analyzer.analyze_resume(resume_text, job_description)
    print_analysis_results(result, "Resume Analysis With Job Description")
    assert result['status'] == 'success'

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s']) 