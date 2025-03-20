"""Scoring utilities for resume analysis."""
from typing import List, Dict

def calculate_star_score(results: List[Dict]) -> float:
    """Calculate overall STAR format score."""
    if not results:
        return 0.0
    
    try:
        complete_count = 0
        for result in results:
            try:
                star_data = result.get("star", {})
                if star_data is not None and isinstance(star_data, dict):
                    complete_count += 1 if star_data.get("complete", False) else 0
            except (AttributeError, TypeError):
                continue
        
        return round((complete_count / len(results)) * 5, 1) if results else 0.0
    except (TypeError, ZeroDivisionError):
        return 0.0

def calculate_metrics_score(results: List[Dict]) -> float:
    """Calculate overall metrics usage score."""
    if not results:
        return 0.0
    
    try:
        metrics_count = 0
        for result in results:
            try:
                metrics = result.get("metrics", [])
                if metrics is not None and isinstance(metrics, list):
                    metrics_count += len(metrics)
            except (AttributeError, TypeError):
                continue
        
        score = (metrics_count / len(results)) * 2.5 if results else 0.0
        return min(5.0, round(score, 1))
    except (TypeError, ZeroDivisionError):
        return 0.0

def calculate_contribution_score(results: List[Dict]) -> float:
    """Calculate overall contribution clarity score."""
    if not results:
        return 0.0
    
    try:
        contribution_scores = []
        for result in results:
            try:
                contribution = result.get("contribution")
                if contribution is not None:
                    score = float(contribution)
                    if 0 <= score <= 5:  # Validate score range
                        contribution_scores.append(score)
            except (TypeError, ValueError, AttributeError):
                continue
        
        return round(sum(contribution_scores) / len(contribution_scores), 1) if contribution_scores else 0.0
    except (TypeError, ZeroDivisionError):
        return 0.0

def calculate_overall_scores(results: List[Dict]) -> Dict:
    """Calculate all scores for the resume."""
    return {
        "starScore": calculate_star_score(results),
        "metricsScore": calculate_metrics_score(results),
        "contributionScore": calculate_contribution_score(results)
    }
