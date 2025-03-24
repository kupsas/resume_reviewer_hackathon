import pytest
from app.services.resume_analyzer.utils.validation import EducationPoint, EducationReputation
from pydantic import ValidationError

def test_valid_education_point():
    """Test that a valid education point passes validation"""
    valid_data = {
        "text": "Bachelor of Science in Computer Science University of California, Berkeley | 2015-2019",
        "subject": "Computer Science",
        "course": "Bachelor of Science",
        "school": "University of California, Berkeley",
        "subject_course_school_reputation": {
            "domestic_score": 9,
            "domestic_score_rationale": "UC Berkeley is one of the top public universities in the US",
            "international_score": 8,
            "international_score_rationale": "UC Berkeley has strong global recognition"
        }
    }
    education_point = EducationPoint(**valid_data)
    assert education_point.text == valid_data["text"]
    assert education_point.subject == valid_data["subject"]
    assert education_point.course == valid_data["course"]
    assert education_point.school == valid_data["school"]
    assert education_point.subject_course_school_reputation.domestic_score == 9

def test_invalid_reputation_score():
    """Test that reputation scores must be between 0 and 10"""
    invalid_data = {
        "text": "Test Education",
        "subject": "Test Subject",
        "course": "Test Course",
        "school": "Test School",
        "subject_course_school_reputation": {
            "domestic_score": 11,  # Invalid score
            "domestic_score_rationale": "Test rationale",
            "international_score": 8,
            "international_score_rationale": "Test rationale"
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        EducationPoint(**invalid_data)
    assert "domestic_score" in str(exc_info.value)

def test_missing_required_fields():
    """Test that required fields cannot be missing"""
    invalid_data = {
        "text": "Test Education",
        # Missing subject, course, school
        "subject_course_school_reputation": {
            "domestic_score": 8,
            "domestic_score_rationale": "Test rationale",
            "international_score": 7,
            "international_score_rationale": "Test rationale"
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        EducationPoint(**invalid_data)
    assert "subject" in str(exc_info.value)
    assert "course" in str(exc_info.value)
    assert "school" in str(exc_info.value)

def test_empty_rationales():
    """Test that rationales cannot be empty strings"""
    invalid_data = {
        "text": "Test Education",
        "subject": "Test Subject",
        "course": "Test Course",
        "school": "Test School",
        "subject_course_school_reputation": {
            "domestic_score": 8,
            "domestic_score_rationale": "",  # Empty rationale
            "international_score": 7,
            "international_score_rationale": "Test rationale"
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        EducationPoint(**invalid_data)
    assert "domestic_score_rationale" in str(exc_info.value)

def test_reputation_model_validation():
    """Test the EducationReputation model specifically"""
    valid_reputation = {
        "domestic_score": 9,
        "domestic_score_rationale": "Test rationale",
        "international_score": 8,
        "international_score_rationale": "Test rationale"
    }
    reputation = EducationReputation(**valid_reputation)
    assert reputation.domestic_score == 9
    assert reputation.international_score == 8

def test_reputation_score_types():
    """Test that reputation scores must be integers"""
    invalid_data = {
        "text": "Test Education",
        "subject": "Test Subject",
        "course": "Test Course",
        "school": "Test School",
        "subject_course_school_reputation": {
            "domestic_score": 8.5,  # Float instead of int
            "domestic_score_rationale": "Test rationale",
            "international_score": 7,
            "international_score_rationale": "Test rationale"
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        EducationPoint(**invalid_data)
    assert "domestic_score" in str(exc_info.value) 