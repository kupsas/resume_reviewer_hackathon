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
                                    "oneOf": [
                                        {
                                            "type": "object",
                                            "properties": {
                                                "text": {"type": "string", "description": "Full text of the point"},
                                                "star": {
                                                    "type": "object",
                                                    "properties": {
                                                        "complete": {"type": "boolean", "description": "Whether STAR format is complete"},
                                                        "missing": {
                                                            "type": "array",
                                                            "items": {"type": "string"},
                                                            "description": "Missing STAR components"
                                                        }
                                                    },
                                                    "required": ["complete", "missing"]
                                                },
                                                "metrics": {
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                    "description": "Identified metrics and achievements"
                                                },
                                                "technical_score": {
                                                    "type": "number",
                                                    "description": "Technical depth score (0-5)",
                                                    "minimum": 0,
                                                    "maximum": 5
                                                },
                                                "improvement": {
                                                    "type": "string",
                                                    "description": "Suggested updated resume point following STAR format and with metrics"
                                                }
                                            },
                                            "required": ["text", "star", "metrics", "technical_score", "improvement"]
                                        },
                                        {
                                            "type": "object",
                                            "properties": {
                                                "text": {"type": "string", "description": "Full text of the education entry"},
                                                "subject": {"type": "string", "description": "Subject/field of study"},
                                                "course": {"type": "string", "description": "Degree/course name"},
                                                "school": {"type": "string", "description": "Institution name"},
                                                "subject_course_school_reputation": {
                                                    "type": "object",
                                                    "properties": {
                                                        "domestic_score": {
                                                            "type": "number",
                                                            "description": "Domestic reputation score (0-10)",
                                                            "minimum": 0,
                                                            "maximum": 10
                                                        },
                                                        "domestic_score_rationale": {
                                                            "type": "string",
                                                            "description": "Explanation for domestic reputation score"
                                                        },
                                                        "international_score": {
                                                            "type": "number",
                                                            "description": "International reputation score (0-10)",
                                                            "minimum": 0,
                                                            "maximum": 10
                                                        },
                                                        "international_score_rationale": {
                                                            "type": "string",
                                                            "description": "Explanation for international reputation score"
                                                        }
                                                    },
                                                    "required": ["domestic_score", "domestic_score_rationale", "international_score", "international_score_rationale"]
                                                }
                                            },
                                            "required": ["text", "subject", "course", "school", "subject_course_school_reputation"]
                                        }
                                    ]
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

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(f"Retrying OpenAI API call after error: {retry_state.outcome.exception()}")
    )
    async def analyze_section(self, section_type: str, text: str) -> Dict[str, Any]:
        """
        Analyze a specific section of a resume.
        
        Args:
            section_type: Type of section (Education, Experience, etc.)
            text: The text content of the section
            
        Returns:
            Dict containing analysis results and token usage
        """
        try:
            # Create section-specific system prompt
            system_prompt = """You are an expert resume analyzer. Analyze the following section of the resume."""
            
            if section_type == "Education":
                system_prompt += """
                For each education entry:
                1. Extract school name, degree, and graduation date
                2. Identify subject/field of study
                3. List relevant coursework and achievements
                4. Provide reputation scores (0-10) for both domestic and international recognition
                5. Include detailed rationales for the reputation scores"""
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                functions=RESUME_ANALYSIS_FUNCTIONS,
                function_call={"name": "analyze_resume_section"},
                temperature=0
            )
            
            # Parse the function call response
            function_response = json.loads(response.choices[0].message.function_call.arguments)
            
            # Extract the relevant section
            section = next(
                (s for s in function_response["sections"] if s["type"] == section_type),
                {"type": section_type, "points": []}
            )
            
            return {
                "status": "success",
                "content": section,
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
            logger.error(f"Error in analyze_section: {str(e)}", exc_info=True)
            # Let tenacity handle the retry
            raise e 