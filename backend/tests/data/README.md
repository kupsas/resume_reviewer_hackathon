# Test Data Directory

This directory contains sample data for testing the Resume Reviewer application.

## Directory Structure

```
data/
├── resumes/           # Sample resumes in different formats
│   ├── sample_resume.pdf   # Sample PDF resume
│   └── sample_resume.docx  # Sample DOCX resume
└── job_descriptions/  # Sample job descriptions
    └── sample_job.txt      # Sample job description
```

## File Descriptions

### Resumes
- `sample_resume.pdf`: A sample resume in PDF format
- `sample_resume.docx`: A sample resume in DOCX format

Both resumes should contain:
- Contact information
- Work experience
- Education
- Skills
- Projects (optional)

### Job Descriptions
- `sample_job.txt`: A sample job description containing:
  - Job title
  - Required skills
  - Responsibilities
  - Qualifications

## Usage

These files are used for:
1. Testing the resume parsing functionality
2. Testing the analysis engine
3. Testing file upload mechanisms
4. Integration testing

## Guidelines

1. Keep test files small but representative
2. Include edge cases where appropriate
3. Don't include sensitive or personal information
4. Update this README when adding new test files 