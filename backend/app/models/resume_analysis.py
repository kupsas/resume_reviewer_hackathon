from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.utils.validation import ResumeAnalysisResponse, TokenUsage

class ResumeAnalysisRequest(BaseModel):
    """Request model for resume analysis."""
    resume_text: str = Field(..., min_length=1, description="The text content of the resume to analyze")
    job_description: Optional[str] = Field(None, description="Optional job description to match against")

# Export the response model from utils
__all__ = ['ResumeAnalysisRequest', 'ResumeAnalysisResponse']

class TokenUsage(BaseModel):
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    total_cost: float

class Scores(BaseModel):
    star_format: float
    metrics_usage: float
    technical_depth: float
    overall: float

class ResumeAnalysis(BaseModel):
    sections: List[Dict[str, Any]]
    scores: Scores
    recommendations: List[str]

class ResumeAnalysisResponse(BaseModel):
    status: str
    resumeAnalysis: ResumeAnalysis
    tokenUsage: TokenUsage
    jobMatchAnalysis: Optional[Dict[str, Any]] = None 