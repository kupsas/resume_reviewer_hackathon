"""Resume analyzer service."""
from typing import Dict, Any, Optional, List
import logging
from openai import AsyncOpenAI
from app.services.openai_service import OpenAIService
from app.core.config import settings

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """Service for analyzing resumes and matching against job descriptions."""
    
    def __init__(self, openai_client: Optional[AsyncOpenAI] = None):
        """Initialize the ResumeAnalyzer with OpenAI client."""
        if openai_client:
            self.openai_service = OpenAIService(openai_client)
        else:
            self.openai_service = OpenAIService(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))
        self.token_usage = {
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0.0
        }
    
    def _update_token_usage(self, usage: Dict[str, Any]) -> None:
        """Update token usage statistics."""
        self.token_usage["total_tokens"] += usage.get("total_tokens", 0)
        self.token_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
        self.token_usage["completion_tokens"] += usage.get("completion_tokens", 0)
        self.token_usage["total_cost"] += usage.get("total_cost", 0.0)
    
    async def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a resume and optionally match against a job description.
        
        Args:
            resume_text: The text content of the resume
            job_description: Optional job description to match against
            
        Returns:
            Dict containing analysis results and token usage
        """
        logger.debug("Starting resume analysis")
        try:
            # Reset token usage for new analysis
            self.token_usage = {
                "total_tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_cost": 0.0
            }
            
            # Analyze resume content
            logger.debug("Calling OpenAI service to analyze resume content")
            resume_analysis = await self.openai_service.analyze_resume_content(resume_text)
            
            if resume_analysis["status"] == "error":
                logger.error(f"Resume analysis failed: {resume_analysis.get('message')}")
                return resume_analysis
            
            # Update token usage
            self._update_token_usage(resume_analysis["token_usage"])
            
            # Pass through OpenAI service response with camelCase keys
            result = {
                "status": resume_analysis["status"],
                "resumeAnalysis": resume_analysis["content"],  # This contains the sections from analyze_resume_section
                "tokenUsage": self.token_usage
            }
            
            # If job description provided, analyze match
            if job_description:
                logger.debug("Job description provided, analyzing match")
                job_match = await self.openai_service.analyze_job_match(resume_text, job_description)
                
                if job_match["status"] == "error":
                    logger.error(f"Job match analysis failed: {job_match.get('message')}")
                    return job_match
                
                # Update token usage
                self._update_token_usage(job_match["token_usage"])
                # Add job match analysis with camelCase
                result["jobMatchAnalysis"] = job_match["content"]
            
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_resume: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "tokenUsage": self.token_usage
            }
