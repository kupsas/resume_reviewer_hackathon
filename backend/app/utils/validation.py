"""Validation utilities for resume analysis."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class TokenUsage(BaseModel):
    """Token usage information."""
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    total_cost: float

class ResumeAnalysisResponse(BaseModel):
    """Complete response model for resume analysis."""
    status: str
    resumeAnalysis: Dict[str, Any]  # Contains sections from analyze_resume_section
    tokenUsage: TokenUsage
    jobMatchAnalysis: Optional[Dict[str, Any]] = None  # Contains job match analysis if provided

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