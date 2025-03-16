from typing import Dict, List, Optional
import docx
from PyPDF2 import PdfReader
from openai import OpenAI
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=self.openai_api_key)

    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file."""
        try:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            if not text.strip():
                raise Exception("No text could be extracted from the PDF")
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict:
        """Analyze resume content using OpenAI API."""
        
        base_scoring_criteria = """
Resume Strength Scoring Criteria:
- Technical Skills (20 points): Quality and relevance of technical abilities
- Experience Quality (20 points): Impact and depth of work history
- Education (20 points): Academic background and certifications
- Resume Format (20 points): Structure, readability, and organization
- Overall Presentation (20 points): Professional impression and clarity
"""

        job_match_criteria = """
Job Match Scoring Criteria:
- Skills Match (25 points): Alignment with required technical skills
- Experience Match (25 points): Match with required experience level and type
- Education Match (20 points): Match with educational requirements
- Requirements Match (20 points): Coverage of specific job requirements
- Overall Fit (10 points): General suitability for the role
""" if job_description else ""

        # Prepare the prompt based on whether a job description is provided
        if job_description:
            prompt = f"""Analyze this resume against the job description and provide detailed feedback. 
Follow this structured format strictly:

{base_scoring_criteria}

{job_match_criteria}

Resume:
{resume_text}

Job Description:
{job_description}

Provide your analysis in exactly this format (do not deviate):

1. RESUME STRENGTH CATEGORIES:
Technical Skills: [number]
Experience Quality: [number]
Education: [number]
Resume Format: [number]
Overall Presentation: [number]

2. RESUME STRENGTH DETAILS:
Technical Skills:
• [Detailed explanation of technical skills score]
• [Specific examples from resume]

Experience Quality:
• [Detailed explanation of experience quality score]
• [Notable achievements or areas for improvement]

Education:
• [Detailed explanation of education score]
• [Analysis of qualifications relevance]

Resume Format:
• [Detailed explanation of format score]
• [Specific formatting feedback]

Overall Presentation:
• [Detailed explanation of presentation score]
• [Specific suggestions if any]

3. FORMAT SUGGESTIONS:
[[ DO NOT INCLUDE THIS IN OUTPUT - this is for context only
The STAR format helps showcase achievements effectively:
- Situation: Set the context of the challenge or opportunity
- Task: Describe the specific responsibility or requirement
- Action: Detail the steps you took to address it
- Result: Quantify the impact with specific metrics (e.g., increased efficiency by 25%, reduced costs by $100K)]]

Examples from your resume to rewrite in STAR format (provide at least 3):
• [Original example from resume]
• [Improved example in STAR format]

General Format Issues:
• [Specific formatting issue and how to fix it]
• [Grammar/punctuation issue and correction]
• [Consistency issue and solution]

4. KEY STRENGTHS (provide at least 3):
- [Strength 1 with brief explanation]
- [Strength 2 with brief explanation]
- [Strength 3 with brief explanation]

5. AREAS FOR IMPROVEMENT (provide at least 3):
- [Area 1 with specific improvement suggestion]
- [Area 2 with specific improvement suggestion]
- [Area 3 with specific improvement suggestion]

6. JOB MATCH CATEGORIES:
Skills Match: [number]
Experience Match: [number]
Education Match: [number]
Requirements Match: [number]
Overall Fit: [number]

7. JOB MATCH DETAILS:
Skills Match:
• [Detailed explanation of skills match score]
• [Specific skills present and missing]

Experience Match:
• [Detailed explanation of experience match]
• [Specific experience alignment points]

Education Match:
• [Detailed explanation of education match]
• [Specific qualifications analysis]

Requirements Match:
• [Detailed explanation of requirements coverage]
• [Key requirements met and gaps]

Overall Fit:
• [Detailed explanation of overall fit]
• [Cultural and professional alignment]

8. JOB-SPECIFIC RECOMMENDATIONS (provide at least 3):
- [Recommendation 1 with specific action items]
- [Recommendation 2 with specific action items]
- [Recommendation 3 with specific action items]
"""
        else:
            prompt = f"""Analyze this resume and provide detailed feedback.
Follow this structured format strictly:

{base_scoring_criteria}

Resume:
{resume_text}

Provide your analysis in exactly this format (do not deviate):

1. RESUME STRENGTH CATEGORIES:
Technical Skills: [number]
Experience Quality: [number]
Education: [number]
Resume Format: [number]
Overall Presentation: [number]

2. RESUME STRENGTH DETAILS:
Technical Skills:
• [Detailed explanation of technical skills score]
• [Specific examples from resume]

Experience Quality:
• [Detailed explanation of experience quality score]
• [Notable achievements or areas for improvement]

Education:
• [Detailed explanation of education score]
• [Analysis of qualifications relevance]

Resume Format:
• [Detailed explanation of format score]
• [Specific formatting feedback]

Overall Presentation:
• [Detailed explanation of presentation score]
• [Specific suggestions if any]

3. FORMAT SUGGESTIONS:
[[ DO NOT INCLUDE THIS IN OUTPUT - this is for context only
The STAR format helps showcase achievements effectively:
- Situation: Set the context of the challenge or opportunity
- Task: Describe the specific responsibility or requirement
- Action: Detail the steps you took to address it
- Result: Quantify the impact with specific metrics (e.g., increased efficiency by 25%, reduced costs by $100K)]]

Examples from your resume to rewrite in STAR format (provide at least 3):
• [Original example from resume]
• [Improved example in STAR format]

General Format Issues:
• [Specific formatting issue and how to fix it]
• [Grammar/punctuation issue and correction]
• [Consistency issue and solution]

4. KEY STRENGTHS (provide at least 3):
- [Strength 1 with brief explanation]
- [Strength 2 with brief explanation]
- [Strength 3 with brief explanation]

5. AREAS FOR IMPROVEMENT (provide at least 3):
- [Area 1 with specific improvement suggestion]
- [Area 2 with specific improvement suggestion]
- [Area 3 with specific improvement suggestion]
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using GPT-3.5 for more consistent responses
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an expert resume reviewer. Follow these rules strictly:
1. Always use the exact format specified in the prompt
2. Return scores as plain numbers only (no text, no '/100', no symbols)
3. Never add explanatory text to scores
4. Never skip any sections
5. Keep responses concise and to the point
6. Always provide STAR format examples with clear Situation, Task, Action, and Result components
7. Extract real achievements from the resume and rewrite them in STAR format
8. Label each STAR component explicitly in the improved examples"""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,  #Zero randomness for consistent responses
                max_tokens=2000,
                presence_penalty=0.0,
                frequency_penalty=0.0
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise Exception("No response received from OpenAI API")
            
            # Parse and standardize the response
            parsed_response = self._parse_openai_response(response.choices[0].message.content, bool(job_description))
            
            return {
                "analysis": parsed_response,
                "status": "success"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"OpenAI API Error: {str(e)}"
            }

    def _parse_openai_response(self, response: str, has_job_description: bool) -> str:
        """Parse and standardize OpenAI response format."""
        try:
            # Split response into sections
            sections = response.split('\n\n')
            parsed_sections = []
            
            for section in sections:
                if section.strip():
                    # Handle the resume strength score section
                    if "RESUME STRENGTH SCORE" in section:
                        try:
                            # Extract just the number from the score section
                            score_lines = section.split('\n')
                            for line in score_lines:
                                if ':' in line:
                                    score = line.split(':')[1].strip()
                                    # Remove any '/100' or other text, keep just the number
                                    score = ''.join(filter(str.isdigit, score))
                                    section = f"RESUME STRENGTH SCORE: {score}"
                                    break
                        except Exception:
                            # If parsing fails, keep the section as is
                            pass
                    
                    # Handle resume strength categories section
                    elif "RESUME STRENGTH CATEGORIES" in section:
                        try:
                            score_lines = section.split('\n')
                            parsed_scores = ["RESUME STRENGTH CATEGORIES:"]
                            for line in score_lines[1:]:  # Skip the header
                                if ':' in line:
                                    category, score = line.split(':')
                                    # Clean up the score to just the number
                                    score = ''.join(filter(str.isdigit, score.strip()))
                                    parsed_scores.append(f"{category.strip()}: {score}")
                            section = '\n'.join(parsed_scores)
                        except Exception:
                            # If parsing fails, keep the section as is
                            pass
                    
                    # Handle job match score section if present
                    elif has_job_description and "JOB MATCH SCORE" in section:
                        try:
                            score_lines = section.split('\n')
                            for line in score_lines:
                                if ':' in line:
                                    score = line.split(':')[1].strip()
                                    score = ''.join(filter(str.isdigit, score))
                                    section = f"JOB MATCH SCORE: {score}"
                                    break
                        except Exception:
                            pass
                    
                    # Handle job match categories section if present
                    elif has_job_description and "JOB MATCH CATEGORIES" in section:
                        try:
                            score_lines = section.split('\n')
                            parsed_scores = ["JOB MATCH CATEGORIES:"]
                            for line in score_lines[1:]:
                                if ':' in line:
                                    category, score = line.split(':')
                                    score = ''.join(filter(str.isdigit, score.strip()))
                                    parsed_scores.append(f"{category.strip()}: {score}")
                            section = '\n'.join(parsed_scores)
                        except Exception:
                            pass
                    
                    parsed_sections.append(section.strip())
            
            # Join sections back together
            return '\n\n'.join(parsed_sections)
        except Exception:
            # If parsing fails, return the original response
            return response 