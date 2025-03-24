"""Response validation utilities for resume analyzer."""
from typing import Dict, List, Any, Optional, Union
import json
from pydantic import BaseModel, Field, validator

class Star(BaseModel):
    """STAR format validation model."""
    situation: bool = Field(..., description="Whether situation is present")
    task: bool = Field(..., description="Whether task is present")
    action: bool = Field(..., description="Whether action is present")
    result: bool = Field(..., description="Whether result is present")
    complete: bool = Field(..., description="Whether all STAR components are present")

    @validator('complete')
    def validate_complete(cls, v: bool, values: Dict) -> bool:
        """Validate that complete is True only if all components are True."""
        if v:
            return all([values.get('situation'), values.get('task'), 
                       values.get('action'), values.get('result')])
        return v

class TokenUsage(BaseModel):
    """Model for token usage statistics."""
    total_tokens: int = Field(..., description="Total tokens used")
    prompt_tokens: int = Field(..., description="Tokens used in prompts")
    completion_tokens: int = Field(..., description="Tokens used in completions")
    total_cost: float = Field(..., description="Total cost in USD")

class AnalysisPoint(BaseModel):
    """Model for validating individual analysis points."""
    text: str = Field(..., description="Original text being analyzed")
    star: Star = Field(..., description="STAR format analysis")
    metrics: List[str] = Field(default_factory=list, description="Extracted metrics")
    technical_score: float = Field(..., ge=0, le=5, description="Technical complexity score")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Suggested improvements")

class EducationReputation(BaseModel):
    """Model for education institution reputation scores."""
    domestic_score: int = Field(..., ge=0, le=10, description="Domestic reputation score (0-10)")
    domestic_score_rationale: str = Field(..., min_length=1, description="Explanation for domestic reputation score")
    international_score: int = Field(..., ge=0, le=10, description="International reputation score (0-10)")
    international_score_rationale: str = Field(..., min_length=1, description="Explanation for international reputation score")

class EducationPoint(BaseModel):
    """Model for validating education section points."""
    text: str = Field(..., description="Full text of the education entry")
    subject: str = Field(..., description="Subject/field of study")
    course: str = Field(..., description="Degree/course name")
    school: str = Field(..., description="Institution name")
    subject_course_school_reputation: EducationReputation = Field(..., description="Reputation scores and rationales")

class EducationAnalysis(BaseModel):
    """Model for validating education section analysis."""
    type: str = Field("Education", description="Section type")
    text: str = Field(..., description="Original education text")
    subject: str = Field(..., description="Field of study")
    course: str = Field(..., description="Type of degree/qualification")
    school: str = Field(..., description="Educational institution")
    subject_course_school_reputation: EducationReputation = Field(..., description="Institution reputation analysis")

class SectionAnalysis(BaseModel):
    """Model for validating section analysis results."""
    type: str = Field(..., description="Section type")
    points: Optional[List[AnalysisPoint]] = Field(None, description="Analysis points for non-education sections")
    summary: str = Field(..., description="Section summary")
    improvement_areas: List[str] = Field(default_factory=list, description="Areas for improvement")
    # Education-specific fields
    text: Optional[str] = Field(None, description="Original education text")
    subject: Optional[str] = Field(None, description="Field of study")
    course: Optional[str] = Field(None, description="Type of degree/qualification")
    school: Optional[str] = Field(None, description="Educational institution")
    subject_course_school_reputation: Optional[EducationReputation] = Field(None, description="Institution reputation analysis")

    @validator('points')
    def validate_points(cls, v: Optional[List[AnalysisPoint]], values: Dict) -> Optional[List[AnalysisPoint]]:
        """Validate that points are present for non-education sections."""
        if values.get('type') != 'Education' and not v:
            raise ValueError("Points are required for non-education sections")
        return v

    @validator('text', 'subject', 'course', 'school', 'subject_course_school_reputation')
    def validate_education_fields(cls, v: Any, values: Dict) -> Any:
        """Validate that education fields are present for education sections."""
        if values.get('type') == 'Education' and not v:
            raise ValueError("Education fields are required for education sections")
        return v

class JobMatchAnalysis(BaseModel):
    """Model for validating job match analysis results."""
    match_score: float = Field(..., ge=0, le=100, description="Overall match score")
    technical_match: Dict[str, Any] = Field(..., description="Technical skills match analysis")
    experience_match: Dict[str, Any] = Field(..., description="Experience requirements match")
    education_match: Dict[str, Any] = Field(..., description="Education requirements match")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")

class ResumeAnalysis(BaseModel):
    """Model for validating resume analysis results."""
    sections: List[Dict[str, Any]] = Field(..., description="Analyzed sections")
    scores: Dict[str, float] = Field(..., description="Analysis scores")
    recommendations: List[str] = Field(..., description="Overall recommendations")

class ResumeAnalysisResponse(BaseModel):
    """Model for validating complete resume analysis response."""
    status: str = Field(..., description="Response status")
    resumeAnalysis: ResumeAnalysis = Field(..., description="Resume analysis results")
    jobMatchAnalysis: Optional[JobMatchAnalysis] = Field(None, description="Optional job match analysis")
    tokenUsage: TokenUsage = Field(..., description="Token usage statistics")

def validate_analysis_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize the analysis response format.
    
    Args:
        response: Raw analysis response dictionary
        
    Returns:
        Validated and normalized response dictionary
        
    Raises:
        ValueError: If response format is invalid
    """
    try:
        # Validate overall response structure
        validated_response = ResumeAnalysisResponse(**response)
        return validated_response.dict()
    except Exception as e:
        raise ValueError(f"Invalid response format: {str(e)}")

def validate_section_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize a single section analysis response.
    
    Args:
        response: Raw section analysis response
        
    Returns:
        Validated and normalized section analysis
        
    Raises:
        ValueError: If section format is invalid
    """
    try:
        validated_section = SectionAnalysis(**response)
        return validated_section.dict()
    except Exception as e:
        raise ValueError(f"Invalid section format: {str(e)}")

def validate_job_match_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize a job match analysis response.
    
    Args:
        response: Raw job match analysis response
        
    Returns:
        Validated and normalized job match analysis
        
    Raises:
        ValueError: If job match format is invalid
    """
    try:
        validated_match = JobMatchAnalysis(**response)
        return validated_match.dict()
    except Exception as e:
        raise ValueError(f"Invalid job match format: {str(e)}") 