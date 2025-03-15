from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import tempfile
import os
from ..services.resume_analyzer import ResumeAnalyzer

router = APIRouter()
analyzer = ResumeAnalyzer()

@router.post("/analyze")
def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: Optional[str] = Form(None)
):
    """
    Analyze a resume file and provide feedback.
    Optionally compare against a job description.
    """
    # Validate file type
    if resume_file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        raise HTTPException(
            status_code=400,
            detail="File must be PDF or DOCX format"
        )

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = resume_file.file.read()
            temp_file.write(content)
            temp_file.seek(0)
            
            # Extract text based on file type
            if resume_file.filename.endswith('.pdf'):
                resume_text = analyzer.extract_text_from_pdf(temp_file.name)
            else:
                resume_text = analyzer.extract_text_from_docx(temp_file.name)

        # Delete temporary file
        os.unlink(temp_file.name)

        # Analyze resume
        analysis_result = analyzer.analyze_resume(resume_text, job_description)
        
        if analysis_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=analysis_result["message"]
            )
            
        return analysis_result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 