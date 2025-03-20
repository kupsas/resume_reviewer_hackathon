"""Resume recommendations generation utilities."""
from typing import List, Dict

def generate_resume_recommendations(analysis_results: List[Dict]) -> List[Dict]:
    """Generate recommendations based on resume analysis."""
    recommendations = []
    
    # Track which sections are present (safely handle malformed results)
    sections = set()
    for result in analysis_results:
        if result and isinstance(result, dict):
            section = result.get("section")
            if section:
                sections.add(section)
    
    # Check for missing key sections
    key_sections = {
        "EXPERIENCE": "Add a work experience section to highlight your professional background.",
        "EDUCATION": "Include an education section to showcase your academic qualifications.",
        "SKILLS": "Add a skills section to highlight your technical and professional competencies."
    }
    
    # Always check for missing key sections
    for section, message in key_sections.items():
        if section not in sections:
            recommendations.append({
                "type": "missing_section",
                "section": section,
                "message": message,
                "priority": 1
            })
    
    # If no valid sections were found, add a general recommendation
    if not sections:
        recommendations.append({
            "type": "general",
            "section": "OVERALL",
            "message": "Add detailed sections about your experience, education, and skills.",
            "priority": 1
        })
    
    # Analyze existing sections
    for result in analysis_results:
        if not result or not isinstance(result, dict):
            continue
            
        section = result.get("section")
        if not section:
            continue
        
        # STAR format recommendations
        star_data = result.get("star", {})
        if isinstance(star_data, dict) and not star_data.get("complete", False):
            recommendations.append({
                "type": "star_format",
                "section": section,
                "message": f"Use STAR format in your {section} section to better describe your achievements.",
                "priority": 2
            })
        
        # Metrics recommendations
        metrics = result.get("metrics", [])
        if isinstance(metrics, list) and not metrics:
            recommendations.append({
                "type": "metrics",
                "section": section,
                "message": f"Add quantifiable metrics in your {section} section to demonstrate impact.",
                "priority": 2
            })
        
        # Contribution clarity recommendations
        contribution = result.get("contribution")
        if isinstance(contribution, (int, float)) and contribution < 3:
            recommendations.append({
                "type": "contribution",
                "section": section,
                "message": f"Clarify your individual contributions in the {section} section.",
                "priority": 3
            })
    
    # Sort recommendations by priority (lower number = higher priority)
    return sorted(recommendations, key=lambda x: x["priority"])

def generate_job_match_recommendations(job_match):
    """Generate recommendations based on job match analysis."""
    if not job_match or "error" in job_match:
        return []
    
    recommendations = []
    
    # Technical skills recommendations
    if job_match["technical_match"]["must_have_skills"]["missing"]:
        missing_skills = ", ".join(job_match["technical_match"]["must_have_skills"]["missing"])
        recommendations.append({
            "type": "technical_skills",
            "message": f"Add experience with: {missing_skills}",
            "priority": "high"
        })
    
    # Experience level recommendations
    if not job_match["experience_match"]["level_match"]:
        recommendations.append({
            "type": "experience_level",
            "message": "Highlight leadership and senior-level responsibilities in your experience",
            "priority": "high"
        })
    
    # Project scale recommendations
    if job_match["project_match"]["scale_match"] < 75:
        recommendations.append({
            "type": "project_scale",
            "message": "Emphasize experience with larger-scale projects",
            "priority": "medium"
        })
    
    return recommendations
