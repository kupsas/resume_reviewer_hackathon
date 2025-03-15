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
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict:
        """Analyze resume content using OpenAI API."""
        
        base_scoring_criteria = """
Scoring Criteria:
- Technical Skills Match (30 points): Relevant programming languages, frameworks, and tools
- Experience Alignment (30 points): Relevant work experience and projects
- Education & Certifications (15 points): Relevant degrees and professional certifications
- Soft Skills & Communication (15 points): Based on how experiences and achievements are articulated
- ATS Compatibility (10 points): Format, keywords, and structure
"""

        # Prepare the prompt based on whether a job description is provided
        if job_description:
            prompt = f"""Analyze this resume against the job description and provide detailed feedback. 
Follow this structured format strictly:

{base_scoring_criteria}

Resume:
{resume_text}

Job Description:
{job_description}

Please provide your analysis in the following format:

1. OVERALL MATCH SCORE (0-100):
[Provide score]
[Break down how the score was calculated using the scoring criteria above]

2. KEY STRENGTHS:
- [Strength 1]
- [Strength 2]
- [etc.]

3. AREAS FOR IMPROVEMENT:
- [Area 1]
- [Area 2]
- [etc.]

4. SECTION-BY-SECTION ANALYSIS:
a) Summary/Objective:
   - Feedback
   - Suggestions
b) Experience:
   - Feedback
   - Suggestions
c) Education:
   - Feedback
   - Suggestions
d) Skills:
   - Feedback
   - Suggestions
e) Projects (if applicable):
   - Feedback
   - Suggestions

5. ATS COMPATIBILITY:
- Format Assessment
- Keyword Analysis
- Structure Recommendations
"""
        else:
            prompt = f"""Analyze this resume and provide detailed feedback.
Follow this structured format strictly:

{base_scoring_criteria}

Resume:
{resume_text}

Please provide your analysis in the following format:

1. OVERALL RESUME STRENGTH SCORE (0-100):
[Provide score]
[Break down how the score was calculated using the scoring criteria above]

2. KEY STRENGTHS:
- [Strength 1]
- [Strength 2]
- [etc.]

3. AREAS FOR IMPROVEMENT:
- [Area 1]
- [Area 2]
- [etc.]

4. SECTION-BY-SECTION ANALYSIS:
a) Summary/Objective:
   - Feedback
   - Suggestions
b) Experience:
   - Feedback
   - Suggestions
c) Education:
   - Feedback
   - Suggestions
d) Skills:
   - Feedback
   - Suggestions
e) Projects (if applicable):
   - Feedback
   - Suggestions

5. ATS COMPATIBILITY:
- Format Assessment
- Keyword Analysis
- Structure Recommendations
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment. You provide detailed, actionable feedback and follow scoring criteria precisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "status": "success"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            } 