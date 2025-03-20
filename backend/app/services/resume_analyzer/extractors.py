"""Text extraction utilities for different file formats."""
from typing import Dict, List, Optional, Any
import docx
from PyPDF2 import PdfReader

def extract_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        if not text.strip():
            raise Exception("No text could be extracted from the PDF")
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
