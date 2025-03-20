from app.services.resume_analyzer import ResumeAnalyzer

def get_resume_analyzer() -> ResumeAnalyzer:
    """
    Dependency to get a ResumeAnalyzer instance.
    """
    return ResumeAnalyzer() 