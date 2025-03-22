# 🔍 API Endpoints Documentation

## Overview
This document outlines the API endpoints we've discovered and tested in our Resume Review application. We'll continue to update this as we discover more endpoints.

## Base URL
- Development: `http://localhost:8000`
- Production: TBD

## Available Endpoints

### 1. Resume Analysis (Text)
**Endpoint:** `/api/resume/analyze`
**Method:** POST
**Description:** Analyzes resume text and provides detailed feedback

#### Request Format
```json
{
    "resume_text": "string",  // Required: The text content of the resume
    "job_description": "string"  // Optional: Job description to match against
}
```

#### Example Request
```json
{
    "resume_text": "John Doe\nSoftware Engineer\n\nEXPERIENCE\nSoftware Engineer at Tech Corp (2020-2022)\n- Developed full-stack applications using React and Node.js\n- Led a team of 3 developers\n\nEDUCATION\nBS in Computer Science, University of Technology (2016-2020)",
    "job_description": "Looking for a Senior Software Engineer with 5+ years of experience in full-stack development and team leadership."
}
```

#### Response Format
```json
{
    "status": "success",
    "resumeAnalysis": {
        "sections": [
            {
                "name": "string",
                "content": "string",
                "score": float
            }
        ],
        "scores": {
            "star_format": float,
            "metrics_usage": float,
            "technical_depth": float,
            "overall": float
        },
        "recommendations": ["string"]
    },
    "tokenUsage": {
        "total_tokens": int,
        "prompt_tokens": int,
        "completion_tokens": int,
        "total_cost": float
    },
    "jobMatchAnalysis": {
        // Optional: Only present if job_description is provided
    }
}
```

#### Example Response
```json
{
    "status": "success",
    "resumeAnalysis": {
        "sections": [
            {
                "name": "Experience",
                "content": "Software Engineer at Tech Corp (2020-2022)\n- Developed full-stack applications using React and Node.js\n- Led a team of 3 developers",
                "score": 0.85
            },
            {
                "name": "Education",
                "content": "BS in Computer Science, University of Technology (2016-2020)",
                "score": 0.9
            }
        ],
        "scores": {
            "star_format": 0.8,
            "metrics_usage": 0.7,
            "technical_depth": 0.85,
            "overall": 0.8
        },
        "recommendations": [
            "Add more quantifiable achievements",
            "Include specific technical skills section",
            "Add relevant certifications"
        ]
    },
    "tokenUsage": {
        "total_tokens": 1500,
        "prompt_tokens": 1000,
        "completion_tokens": 500,
        "total_cost": 0.02
    }
}
```

### 2. Resume Analysis (File)
**Endpoint:** `/api/resume/analyze/file`
**Method:** POST
**Description:** Analyzes a resume file (PDF or DOCX) and provides detailed feedback

#### Request Format
- Content-Type: `multipart/form-data`
- Parameters:
  - `file`: PDF or DOCX file (required)
  - `job_description`: string (optional)

#### Response Format
Same as the text analysis endpoint

### 3. Health Check
**Endpoint:** `/health`
**Method:** GET
**Description:** Verifies if the API is up and running

#### Response Format
```json
{
    "status": "healthy"
}
```

#### Status Codes
- 200: Service is healthy
- 503: Service is unavailable

## Error Responses
All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "status": "error",
    "detail": "Error message describing the issue"
}
```

### 500 Internal Server Error
```json
{
    "status": "error",
    "detail": "Error message describing the issue",
    "code": "INTERNAL_SERVER_ERROR",
    "tokenUsage": {}
}
```

## Testing Notes
- We've successfully tested both text and file analysis endpoints
- The analysis endpoints typically respond within 2-3 seconds
- The health check endpoint responds almost instantly
- File upload supports PDF and DOCX formats
- Job description matching is optional but provides additional insights

## Next Steps
- [x] Add example requests and responses for each endpoint
- [x] Document error responses
- [ ] Add rate limiting information
- [ ] Document authentication requirements (if any)
- [ ] Add more example responses with different resume types

## 🔄 Updates
- Initial documentation created based on testing experience
- Updated to match actual backend implementation
- Added file upload endpoint documentation
- Added detailed error response documentation 