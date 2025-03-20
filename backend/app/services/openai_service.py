"""OpenAI service for resume analysis."""
from typing import Dict, Any, List, Optional
import json
import logging
import httpx
from openai import AsyncOpenAI
from app.core.config import settings
import tenacity

logger = logging.getLogger(__name__)

# Function schemas for OpenAI API
RESUME_ANALYSIS_FUNCTIONS = [
    {
        "name": "analyze_resume_section",
        "description": "Analyze different sections of a resume",
        "parameters": {
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "description": "Type of section (Experience, Projects, Education, Skills)"},
                            "points": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string", "description": "Original bullet point text"},
                                        "star": {
                                            "type": "object",
                                            "properties": {
                                                "situation": {"type": "boolean"},
                                                "task": {"type": "boolean"},
                                                "action": {"type": "boolean"},
                                                "result": {"type": "boolean"},
                                                "complete": {"type": "boolean"}
                                            },
                                            "required": ["situation", "task", "action", "result", "complete"]
                                        },
                                        "metrics": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of metrics found in the point"
                                        },
                                        "technical_score": {
                                            "type": "number",
                                            "minimum": 0,
                                            "maximum": 5,
                                            "description": "Technical depth score (0-5)"
                                        },
                                        "improvement": {
                                            "type": "string",
                                            "description": "Suggested updated resume point following STAR format and with metrics"
                                        }
                                    },
                                    "required": ["text", "star", "metrics", "technical_score", "improvement"]
                                }
                            }
                        },
                        "required": ["type", "points"]
                    }
                }
            },
            "required": ["sections"]
        }
    }
]

JOB_MATCH_FUNCTIONS = [
    {
        "name": "analyze_job_match",
        "description": "Analyze how well a resume matches a job description",
        "parameters": {
            "type": "object",
            "properties": {
                "match_score": {"type": "number", "minimum": 0, "maximum": 100},
                "technical_match": {
                    "type": "object",
                    "properties": {
                        "matched_skills": {"type": "array", "items": {"type": "string"}},
                        "missing_skills": {"type": "array", "items": {"type": "string"}},
                        "skill_coverage_score": {"type": "number", "minimum": 0, "maximum": 100}
                    }
                },
                "experience_match": {
                    "type": "object",
                    "properties": {
                        "required_years": {"type": "integer"},
                        "actual_years": {"type": "integer"},
                        "experience_score": {"type": "number", "minimum": 0, "maximum": 100}
                    }
                },
                "key_requirements": {
                    "type": "object",
                    "properties": {
                        "met": {"type": "array", "items": {"type": "string"}},
                        "partially_met": {"type": "array", "items": {"type": "string"}},
                        "not_met": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "section_recommendations": {
                    "type": "object",
                    "properties": {
                        "experience_projects": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "original_point": {"type": "string"},
                                    "improved_version": {"type": "string"}
                                }
                            }
                        },
                        "education": {"type": "string"},
                        "skills_certs": {"type": "string"}
                    }
                },
                "recommendations": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["match_score", "technical_match", "experience_match", "key_requirements", "section_recommendations", "recommendations"]
        }
    }
]

class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self, client: Optional[AsyncOpenAI] = None):
        """Initialize the OpenAI service."""
        if client:
            self.client = client
        else:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                max_retries=3,
                timeout=60.0
            )

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(f"Retrying OpenAI API call after error: {retry_state.outcome.exception()}")
    )
    async def analyze_resume_content(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume content using function calling.
        
        Args:
            resume_text: The text content of the resume
            
        Returns:
            Dict containing analysis results and token usage
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
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
            
            # Parse the function call response
            function_response = json.loads(response.choices[0].message.function_call.arguments)
            
            return {
                "status": "success",
                "content": function_response,
                "token_usage": {
                    "total_tokens": response.usage.total_tokens,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_cost": (
                        response.usage.prompt_tokens * settings.COST_PER_INPUT_TOKEN +
                        response.usage.completion_tokens * settings.COST_PER_OUTPUT_TOKEN
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_resume_content: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "token_usage": {
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_cost": 0
                }
            }
    
    async def analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze how well a resume matches a job description.
        
        Args:
            resume_text: The text content of the resume
            job_description: The job description to match against
            
        Returns:
            Dict containing match analysis and token usage
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
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
   - Provide one-sentence recommendation on how to better present coursework to match the job
   - Provide one-sentence recommendation on how to better present projects to match the job
   - Provide one-sentence recommendation on how to better present co-curriculars to match the job

3. For Skills/Certifications section:
   - Provide one-sentence recommendation on how to better present skills and certifications to match the job"""
                    },
                    {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"}
                ],
                functions=JOB_MATCH_FUNCTIONS,
                function_call={"name": "analyze_job_match"},
                temperature=0
            )
            
            # Parse the function call response
            function_response = json.loads(response.choices[0].message.function_call.arguments)
            
            return {
                "status": "success",
                "content": function_response,
                "token_usage": {
                    "total_tokens": response.usage.total_tokens,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_cost": (
                        response.usage.prompt_tokens * settings.COST_PER_INPUT_TOKEN +
                        response.usage.completion_tokens * settings.COST_PER_OUTPUT_TOKEN
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_job_match: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "token_usage": {
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_cost": 0
                }
            } 