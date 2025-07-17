from app.services.resume_analyzer import ResumeAnalyzer

# Global instance to share cache across requests
_resume_analyzer_instance = None

def get_resume_analyzer() -> ResumeAnalyzer:
    """
    Dependency to get a ResumeAnalyzer instance.
    Uses singleton pattern to share cache across requests.
    """
    global _resume_analyzer_instance
    if _resume_analyzer_instance is None:
        _resume_analyzer_instance = ResumeAnalyzer()
    return _resume_analyzer_instance 