"""Validation utilities for resume analysis."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TokenUsage(BaseModel):
    """Token usage information."""
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    total_cost: float

class TechnicalMatch(BaseModel):
    """Technical skills match information."""
    matched_skills: List[str]
    missing_skills: List[str]
    skill_coverage_score: float = Field(ge=0, le=100)

class ExperienceMatch(BaseModel):
    """Experience match information."""
    required_years: int
    actual_years: int
    experience_score: float = Field(ge=0, le=100)

class KeyRequirements(BaseModel):
    """Key requirements match information."""
    met: List[str]
    partially_met: List[str]
    not_met: List[str]

class JobMatchAnalysis(BaseModel):
    """Model for job match analysis."""
    match_score: float = Field(ge=0, le=100)
    technical_match: TechnicalMatch
    experience_match: ExperienceMatch
    key_requirements: KeyRequirements
    recommendations: List[str]

class ResumeAnalysisResponse(BaseModel):
    """Complete response model for resume analysis."""
    status: str
    resumeAnalysis: Dict[str, Any]  # Contains sections from analyze_resume_section
    tokenUsage: TokenUsage
    jobMatchAnalysis: Optional[JobMatchAnalysis] = None  # Contains job match analysis if provided

def validate_analysis_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the analysis response against the schema.
    
    Args:
        response: The response dictionary to validate
        
    Returns:
        Dict[str, Any]: The validated response or error message
    """
    try:
        # Create a response object and validate
        validated = ResumeAnalysisResponse(**response)
        return validated.model_dump()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Response validation failed: {str(e)}"
        } 