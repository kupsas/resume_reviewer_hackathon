"""Response validation utilities for resume analyzer."""
from typing import Dict, List, Any, Optional, Union
import json
from pydantic import BaseModel, Field, validator

class Star(BaseModel):
    """STAR format validation model."""
    situation: bool = Field(..., description="Whether situation is present")
    situation_rationale: str = Field(..., description="Explanation for situation assessment")
    action: bool = Field(..., description="Whether action is present")
    action_rationale: str = Field(..., description="Explanation for action assessment")
    result: bool = Field(..., description="Whether result is present")
    result_rationale: str = Field(..., description="Explanation for result assessment")
    complete: bool = Field(..., description="Whether all STAR components are present")

    @validator('complete')
    def validate_complete(cls, v: bool, values: Dict) -> bool:
        """Validate that complete is True only if all components are True."""
        if v:
            return all([values.get('situation'), values.get('action'), values.get('result')])
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

def validate_star_components(star: Dict[str, Any]) -> Dict[str, Any]:
    """Validate STAR components in a resume point."""
    required_fields = [
        "situation", "situation_rationale",
        "action", "action_rationale",
        "result", "result_rationale",
        "complete"
    ]
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in star]
    if missing_fields:
        raise ValueError(f"Missing required STAR fields: {', '.join(missing_fields)}")
    
    # Validate field types
    if not isinstance(star["situation"], bool):
        raise ValueError("situation must be a boolean")
    if not isinstance(star["action"], bool):
        raise ValueError("action must be a boolean")
    if not isinstance(star["result"], bool):
        raise ValueError("result must be a boolean")
    if not isinstance(star["complete"], bool):
        raise ValueError("complete must be a boolean")
    if not isinstance(star["situation_rationale"], str):
        raise ValueError("situation_rationale must be a string")
    if not isinstance(star["action_rationale"], str):
        raise ValueError("action_rationale must be a string")
    if not isinstance(star["result_rationale"], str):
        raise ValueError("result_rationale must be a string")
    
    # Validate rationale lengths
    if len(star["situation_rationale"]) < 10:
        raise ValueError("situation_rationale must be at least 10 characters")
    if len(star["action_rationale"]) < 10:
        raise ValueError("action_rationale must be at least 10 characters")
    if len(star["result_rationale"]) < 10:
        raise ValueError("result_rationale must be at least 10 characters")
    
    return star

def validate_resume_point(point: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single resume point."""
    required_fields = ["text", "star", "metrics", "technical_score", "improvement"]
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in point]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate text
    if not isinstance(point["text"], str) or not point["text"].strip():
        raise ValueError("text must be a non-empty string")
    
    # Validate STAR components
    point["star"] = validate_star_components(point["star"])
    
    # Validate metrics
    if not isinstance(point["metrics"], list):
        raise ValueError("metrics must be a list")
    for metric in point["metrics"]:
        if not isinstance(metric, str):
            raise ValueError("each metric must be a string")
    
    # Validate technical score
    if not isinstance(point["technical_score"], (int, float)):
        raise ValueError("technical_score must be a number")
    if not 0 <= point["technical_score"] <= 5:
        raise ValueError("technical_score must be between 0 and 5")
    
    # Validate improvement
    if not isinstance(point["improvement"], str):
        raise ValueError("improvement must be a string")
    
    return point

def validate_education_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate an education entry."""
    required_fields = ["text", "subject", "course", "school", "subject_course_school_reputation"]
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in entry]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate text
    if not isinstance(entry["text"], str) or not entry["text"].strip():
        raise ValueError("text must be a non-empty string")
    
    # Validate subject
    if not isinstance(entry["subject"], str) or not entry["subject"].strip():
        raise ValueError("subject must be a non-empty string")
    
    # Validate course
    if not isinstance(entry["course"], str) or not entry["course"].strip():
        raise ValueError("course must be a non-empty string")
    
    # Validate school
    if not isinstance(entry["school"], str) or not entry["school"].strip():
        raise ValueError("school must be a non-empty string")
    
    # Validate reputation scores
    rep = entry["subject_course_school_reputation"]
    required_rep_fields = [
        "domestic_score", "domestic_score_rationale",
        "international_score", "international_score_rationale"
    ]
    
    missing_rep_fields = [field for field in required_rep_fields if field not in rep]
    if missing_rep_fields:
        raise ValueError(f"Missing required reputation fields: {', '.join(missing_rep_fields)}")
    
    # Validate score types and ranges
    if not isinstance(rep["domestic_score"], (int, float)):
        raise ValueError("domestic_score must be a number")
    if not isinstance(rep["international_score"], (int, float)):
        raise ValueError("international_score must be a number")
    if not 0 <= rep["domestic_score"] <= 10:
        raise ValueError("domestic_score must be between 0 and 10")
    if not 0 <= rep["international_score"] <= 10:
        raise ValueError("international_score must be between 0 and 10")
    
    # Validate rationale types and lengths
    if not isinstance(rep["domestic_score_rationale"], str):
        raise ValueError("domestic_score_rationale must be a string")
    if not isinstance(rep["international_score_rationale"], str):
        raise ValueError("international_score_rationale must be a string")
    if len(rep["domestic_score_rationale"]) < 10:
        raise ValueError("domestic_score_rationale must be at least 10 characters")
    if len(rep["international_score_rationale"]) < 10:
        raise ValueError("international_score_rationale must be at least 10 characters")
    
    return entry

def validate_section_response(section: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a section response from the resume analysis."""
    required_fields = ["type", "points"]
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in section]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate type
    if not isinstance(section["type"], str):
        raise ValueError("type must be a string")
    
    # Validate points
    if not isinstance(section["points"], list):
        raise ValueError("points must be a list")
    
    # Validate each point based on section type
    if section["type"] == "Education":
        section["points"] = [validate_education_entry(point) for point in section["points"]]
    else:
        section["points"] = [validate_resume_point(point) for point in section["points"]]
    
    return section

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