from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import tempfile
import os
import logging
from app.services.resume_analyzer import ResumeAnalyzer
from app.models.resume_analysis import ResumeAnalysisRequest
from app.utils.validation import ResumeAnalysisResponse, validate_analysis_response
from app.dependencies import get_resume_analyzer
from app.utils.file_utils import extract_text_from_pdf, extract_text_from_docx

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    request: ResumeAnalysisRequest,
    analyzer: ResumeAnalyzer = Depends(get_resume_analyzer)
) -> Dict[str, Any]:
    """
    Analyze a resume text and optionally match against a job description.
    """
    logger.debug("Starting resume analysis")
    try:
        # Validate input
        if not request.resume_text.strip():
            logger.warning("Empty resume text provided")
            raise HTTPException(
                status_code=400,
                detail="Empty resume text provided"
            )

        result = await analyzer.analyze_resume(
            resume_text=request.resume_text,
            job_description=request.job_description if request.job_description else None
        )
        
        if result.get("status") == "error":
            logger.error(f"Analysis failed: {result.get('message')}")
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Analysis failed")
            )
            
        # Validate the response format
        validated_response = validate_analysis_response(result)
        if validated_response.get("status") == "error":
            logger.error(f"Response validation failed: {validated_response.get('message')}")
            raise HTTPException(
                status_code=500,
                detail=f"Invalid analysis response format: {validated_response.get('message')}"
            )
            
        return validated_response
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze_resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/analyze/file", response_model=ResumeAnalysisResponse)
async def analyze_resume_file(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    analyzer: ResumeAnalyzer = Depends(get_resume_analyzer)
) -> Dict[str, Any]:
    """
    Analyze a resume file (PDF or DOCX) and provide detailed feedback.
    """
    temp_file_path = ""
    logger.debug(f"Starting file analysis for {file.filename}")
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            logger.warning(f"Invalid file type: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a PDF or DOCX file."
            )

        # Save uploaded file
        suffix = '.pdf' if file.filename.lower().endswith('.pdf') else '.docx'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        try:
            # Extract text based on file type
            if temp_file_path.lower().endswith('.pdf'):
                resume_text = extract_text_from_pdf(temp_file_path)
            else:  # .docx
                resume_text = extract_text_from_docx(temp_file_path)

            if not resume_text or not resume_text.strip():
                logger.error("Empty text extracted from file")
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract text from the uploaded file"
                )

            # Analyze the extracted text
            result = await analyzer.analyze_resume(resume_text, job_description)
            
            # Validate response format
            validated_response = validate_analysis_response(result)
            if validated_response.get("status") == "error":
                logger.error(f"Response validation failed: {validated_response.get('message')}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Invalid analysis response format: {validated_response.get('message')}"
                )
                
            return validated_response

        except ValueError as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract text from file: {str(e)}"
            )

    except Exception as e:
        logger.error(f"Unexpected error in analyze_resume_file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file {temp_file_path}: {str(e)}") 