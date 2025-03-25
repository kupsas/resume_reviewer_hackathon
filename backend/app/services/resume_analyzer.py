from typing import Dict, List, Optional, Any, Tuple
import docx
from PyPDF2 import PdfReader
from openai import AsyncOpenAI
from pathlib import Path
import os
from dotenv import load_dotenv
import json
import uuid
import asyncio
import re
from .openai_service import RESUME_ANALYSIS_FUNCTIONS, JOB_MATCH_FUNCTIONS
from app.core.config import settings
from .resume_formats import (
    POINT_EXTRACTION_FORMAT,
    RESUME_ANALYSIS_FORMAT,
    JOB_MATCH_FORMAT,
    INTEGRATED_IMPROVEMENTS_FORMAT
)
from .openai_service import OpenAIService

load_dotenv()

class ResumeAnalyzer:
    """
    A class to analyze resumes using OpenAI's GPT models.
    Provides functionality for resume analysis, job matching, and generating improvements.
    """
    
    def __init__(self, openai_client: Optional[AsyncOpenAI] = None):
        """Initialize the ResumeAnalyzer with OpenAI client and configurations."""
        # Initialize OpenAI client
        self.client = openai_client or AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create OpenAI service instance
        self.openai_service = OpenAIService(client=self.client)
        
        # Model configuration - using standard OpenAI models
        self.model = settings.OPENAI_MODEL  # Use model from settings
        
        # Initialize token usage tracking
        self.token_usage = {
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0
        }
        
        # System messages for different analyses
        self.system_messages = {
            "analysis": """You are an expert resume analyzer with deep experience in technical recruitment and career coaching. 
Analyze each bullet point for:
1. STAR Format components with STRICT criteria - do not assume anything is implied unless it is extremely obvious:
   * Situation (S): Should clearly describe the context or scenario with minimal ambiguity. Should answer the questions "What was the challenge you faced?" or "WHY did you perform the action?". If either of these criteria is met, mention clearly. If not, mention which is not met.
   * Action (A): Should describe specific actions taken with concrete methodology. Should answer the questions "What did you do to face the challenge?" or "WHAT did you do to achieve the result?". If either of these criteria is met, mention clearly. If not, mention which is not met.  
   * Result (R): Should clearly indicate the outcome with quantifiable metrics and numbers. Should answer the questions "What metric did you move by doing the task?" or "What was the indicator of your success in the action / in the situation?". If either of these criteria is met, mention clearly. If not, mention which is not met.
2. Metrics and quantifiable achievements
3. Technical depth and complexity
4. Individual vs team contributions
Return detailed analysis in JSON format with rationale for each assessment.""",

            "education": """You are an expert resume analyzer. Analyze the provided education section and return a JSON response.

For Education section:
- Extract and analyze:
  * Subject: The specific field of study (e.g., Computer Science, Business Administration)
  * Course: The type of degree or qualification (e.g., Bachelor of Science, MBA)
  * School: The educational institution name
- Evaluate institution reputation:
  * Domestic score (1-10) based on:
    - National rankings and academic excellence
    - Research output and impact
    - Industry connections and partnerships
    - Program-specific reputation
    - Alumni network strength
  * International score (1-10) based on:
    - Global university rankings
    - International research collaborations
    - Global recognition and partnerships
    - International student/faculty diversity
    - Cross-border academic programs
  * Provide detailed rationale for each score
- Include any additional details like GPA, relevant coursework, or achievements

Return analysis in JSON format following the specified schema.""",

            "job_match": """Expert technical recruiter analyzing resume-job fit. Focus on:
1. Technical skills alignment
2. Experience relevance
3. Project complexity match
4. Missing critical requirements
5. Overall recommendations for improvement
Return detailed JSON analysis with specific examples."""
        }

    # ===== Core Analysis Methods =====

    async def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point for resume analysis. Performs comprehensive analysis including:
        - Section identification and analysis
        - STAR format checking
        - Metrics extraction
        - Job matching (if job description provided)
        """
        if not resume_text or resume_text.strip() == "":
            raise ValueError("Resume text cannot be empty")

        try:
            # Extract and analyze sections
            sections = self._split_resume_into_sections(resume_text)
            
            # Analyze sections using OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_messages["analysis"]},
                    {"role": "user", "content": f"Analyze the following resume sections:\n\n{resume_text}"}
                ],
                functions=RESUME_ANALYSIS_FUNCTIONS,
                function_call={"name": "analyze_resume_section"}
            )

            # Extract analysis results
            analysis_result = json.loads(response.choices[0].message.function_call.arguments)
            
            # Update token usage
            self._update_token_usage(response)

            # If job description is provided, perform job matching
            job_match_result = None
            if job_description:
                if not job_description.strip():
                    raise ValueError("Job description cannot be empty")
                    
                # Use the OpenAI service's analyze_job_match method
                job_match_result = await self.openai_service.analyze_job_match(resume_text, job_description)

            # Prepare final response
            result = {
                "status": "success",
                "resumeAnalysis": analysis_result,
                "tokenUsage": self.token_usage.copy()
            }

            if job_match_result:
                if job_match_result["status"] == "error":
                    logger.error(f"Job match analysis failed: {job_match_result.get('message')}")
                    result["jobMatchAnalysis"] = job_match_result
                else:
                    # Update token usage
                    self._update_token_usage(job_match_result["token_usage"])
                    # Add job match analysis with camelCase
                    result["jobMatchAnalysis"] = job_match_result["content"]

            return result

        except Exception as e:
            logger.error(f"Error in analyze_resume: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "sections": [],
                "tokenUsage": self.token_usage.copy()
            }

    async def analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Dedicated method for job matching analysis."""
        try:
            # Extract job requirements
            requirements = await self._extract_job_requirements(job_description)
            
            # Perform detailed matching
            match_result = await self._perform_job_matching(resume_text, requirements)
            
            return {
                "status": "success",
                "matchAnalysis": match_result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    # ===== Section Analysis Methods =====

    def _split_resume_into_sections(self, resume_text: str) -> str:
        """Split resume text into sections for analysis."""
        # Simple preprocessing to clean the text
        cleaned_text = resume_text.strip()
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)  # Normalize multiple newlines
        return cleaned_text

    async def _analyze_sections(self, sections: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Analyze each section with appropriate analysis type."""
        results = []
        
        for section in sections:
            if section["type"] == "EDUCATION":
                result = await self._analyze_education(section["content"])
            else:
                result = await self._analyze_general_section(section["content"], section["type"])
            results.append(result)
        
        return results

    async def _analyze_education(self, content: str) -> Dict[str, Any]:
        """Analyze education section with specialized focus."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_messages["education"]},
                    {"role": "user", "content": f"Analyze this education section:\n{content}"}
                ],
                functions=RESUME_ANALYSIS_FUNCTIONS,
                function_call={"name": "analyze_resume_section"},
                temperature=0
            )
            
            # Parse the function call response
            analysis_result = json.loads(response.choices[0].message.function_call.arguments)
            
            # Update token usage
            self._update_token_usage(response)
            
            # Validate the response using our new schema
            from app.services.resume_analyzer.utils.validation import validate_section_response
            validated_result = validate_section_response({
                "type": "Education",
                "text": content,
                **analysis_result["sections"][0]  # Extract the first section's data
            })
            
            return validated_result
            
        except Exception as e:
            logger.error(f"Error in _analyze_education: {str(e)}", exc_info=True)
            return {
                "type": "Education",
                "text": content,
                "error": str(e)
            }

    async def _analyze_general_section(self, content: str, section_type: str) -> Dict[str, Any]:
        """Analyze non-education sections focusing on STAR format and metrics."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_messages["analysis"]},
                {"role": "user", "content": f"Analyze this {section_type} section:\n{content}"}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        self._update_token_usage(response)
        return json.loads(response.choices[0].message.content)

    # ===== Job Matching Methods =====

    async def _extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract structured requirements from job description."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """Extract key job requirements focusing on:
1. Technical skills (required vs preferred)
2. Experience level and domain expertise
3. Project complexity and scale
4. Soft skills and qualifications"""
                },
                {"role": "user", "content": job_description}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        self._update_token_usage(response)
        return json.loads(response.choices[0].message.content)

    async def _perform_job_matching(self, resume_text: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Match resume against extracted job requirements."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_messages["job_match"]},
                {
                    "role": "user",
                    "content": f"""Compare this resume against the job requirements:
Resume: {resume_text}
Requirements: {json.dumps(requirements, indent=2)}"""
                }
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        self._update_token_usage(response)
        return json.loads(response.choices[0].message.content)

    # ===== Utility Methods =====

    def _update_token_usage(self, response: Any) -> None:
        """Update token usage statistics from API response."""
        if hasattr(response, 'usage'):
            self.token_usage["prompt_tokens"] += response.usage.prompt_tokens
            self.token_usage["completion_tokens"] += response.usage.completion_tokens
            self.token_usage["total_tokens"] += response.usage.total_tokens
            
            # Calculate costs based on model pricing
            prompt_cost = (response.usage.prompt_tokens / 1000) * 0.01  # $0.01 per 1K tokens
            completion_cost = (response.usage.completion_tokens / 1000) * 0.03  # $0.03 per 1K tokens
            self.token_usage["total_cost"] += prompt_cost + completion_cost

    def _calculate_scores(self, sections: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate various scores from the analysis results."""
        total_points = 0
        star_complete = 0
        metrics_count = 0
        technical_score_sum = 0
        education_score_sum = 0
        education_count = 0

        for section in sections:
            if section["type"] == "Education":
                # Handle education sections
                if "subject_course_school_reputation" in section:
                    rep = section["subject_course_school_reputation"]
                    # Calculate education score as average of domestic and international scores
                    education_score = (rep["domestic_score"] + rep["international_score"]) / 2
                    education_score_sum += education_score
                    education_count += 1
            else:
                # Handle regular sections
                for point in section.get("points", []):
                    total_points += 1
                    if point.get("star", {}).get("complete", False):
                        star_complete += 1
                    metrics_count += len(point.get("metrics", []))
                    technical_score_sum += point.get("technical_score", 0)

        # Calculate average scores
        star_score = (star_complete / total_points) * 5 if total_points > 0 else 0
        metrics_score = min(5, metrics_count / total_points * 2.5) if total_points > 0 else 0
        technical_score = technical_score_sum / total_points if total_points > 0 else 0
        education_score = education_score_sum / education_count if education_count > 0 else 0

        return {
            "star_format": round(star_score, 2),
            "metrics_usage": round(metrics_score, 2),
            "technical_depth": round(technical_score, 2),
            "education_quality": round(education_score, 2),
            "overall": round((star_score + metrics_score + technical_score + education_score) / 4, 2)
        }

    def _generate_recommendations(self, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate prioritized recommendations based on analysis."""
        recommendations = []
        
        # Analyze STAR format usage
        star_missing = []
        metrics_missing = []
        technical_weak = []
        education_weak = []
        
        for result in analysis_results:
            if result["type"] == "Education":
                # Analyze education quality
                if "subject_course_school_reputation" in result:
                    rep = result["subject_course_school_reputation"]
                    avg_score = (rep["domestic_score"] + rep["international_score"]) / 2
                    if avg_score < 7:
                        education_weak.append({
                            "school": result.get("school", "Unknown Institution"),
                            "score": round(avg_score, 1),
                            "rationale": f"Domestic: {rep['domestic_score_rationale']}, International: {rep['international_score_rationale']}"
                        })
            else:
                # Analyze regular sections
                for point in result.get("points", []):
                    star = point.get("star", {})
                    if not star.get("complete", False):
                        star_missing.append({
                            "text": point["text"],
                            "rationale": {
                                "situation": star.get("situation_rationale", ""),
                                "action": star.get("action_rationale", ""),
                                "result": star.get("result_rationale", "")
                            }
                        })
                    if not point.get("metrics", []):
                        metrics_missing.append(point["text"])
                    if float(point.get("technical_score", 0)) < 3:
                        technical_weak.append(point["text"])
        
        # Generate recommendations
        if star_missing:
            recommendations.append({
                "priority": "high",
                "area": "STAR Format",
                "action": "Add missing STAR components to key achievements",
                "examples": star_missing[:2],  # Show first 2 examples with rationales
                "rationale": "Missing STAR components identified with detailed explanations"
            })
        
        if metrics_missing:
            recommendations.append({
                "priority": "high",
                "area": "Metrics",
                "action": "Add quantifiable metrics to demonstrate impact",
                "examples": metrics_missing[:2]
            })
        
        if technical_weak:
            recommendations.append({
                "priority": "medium",
                "area": "Technical Depth",
                "action": "Enhance technical details in project descriptions",
                "examples": technical_weak[:2]
            })
        
        if education_weak:
            recommendations.append({
                "priority": "medium",
                "area": "Education Quality",
                "action": "Consider pursuing additional certifications or advanced degrees to strengthen your academic profile",
                "examples": [f"{edu['school']} (Current Score: {edu['score']}/10, Rationale: {edu['rationale']})" for edu in education_weak[:2]]
            })
        
        return recommendations

    def get_token_usage(self) -> Dict[str, Any]:
        """Get current token usage statistics."""
        return self.token_usage.copy()

#What do I want to see from the resume analysis?

#RESUME ANALYSIS
#- A resume strength score is useless for most people as it doesn't tell them what to do with the feedback.
#- I want to see what is good about the resume: has the candidate mentioned their skills well? have they used STAR format? have they mentioned outcomes for each resume point? have they mentioned metrics? 
#- I want to see projects where the candidate has individually contributed v group projects.
#- I want all formatting and grammatical errors called out clearly.
#- I want to see corrected / improved examples of points from the resume.

#JOB DESCRIPTION <> RESUME MATCHING
#- I want to see how well the resume matches the job description - includes tech skills (tools, technology, etc.), soft skills (has the candidate done B2B sales, or project management), industries they have worked in, etc.
#- I want to see how the resume can be improved to match the job description.