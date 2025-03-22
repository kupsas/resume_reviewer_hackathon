# Resume Analyzer Backend 🎯

A powerful FastAPI-based backend service that analyzes resumes against job descriptions using AI. This service provides detailed feedback on resume content, STAR format analysis, and job match scoring.

## Features ✨

- Resume analysis with detailed section breakdown
- STAR format evaluation for experience points
- Technical depth scoring
- Job match analysis
- Metrics extraction
- Cost-effective token usage tracking
- Support for PDF, DOCX, and TXT file formats

## Prerequisites 🛠️

- Python 3.11 (recommended)
- OpenAI API key
- Virtual environment (recommended)

## Installation 🚀

1. Clone the repository:
```bash
git clone <repository-url>
cd ResumeReviewer
```

2. Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your OpenAI API key
```

## Running the Server 🏃‍♂️

1. Start the FastAPI server:
```bash
cd backend
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`

## Testing the Backend 🧪

1. Make sure the server is running
2. Run the test script:
```bash
cd backend
python test_actual_resume.py
```

The test script will:
- Read sample resume and job description
- Send them for analysis
- Display detailed results including:
  - Job match score
  - Technical match analysis
  - STAR format evaluation
  - Metrics extraction
  - Resource usage statistics

## API Endpoints 🔌

### POST /api/resume/analyze

Analyzes a resume against a job description.

Request body:
```json
{
    "resume_text": "string",
    "job_description": "string"
}
```

Response includes:
- Resume analysis with section breakdown
- STAR format evaluation
- Technical depth scoring
- Job match analysis
- Recommendations
- Token usage statistics

## Sample Files 📄

The backend includes sample files for testing:
- `tests/data/resumes/sample_resume.pdf`
- `tests/data/job_descriptions/sample_job.txt`

## Resource Usage 💰

The service tracks token usage and provides cost estimates for each analysis:
- Total tokens used
- Prompt tokens
- Completion tokens
- Estimated cost

## Error Handling 🚨

The service includes comprehensive error handling for:
- File reading errors
- API connection issues
- Invalid input formats
- Rate limiting

## Development 🔧

To contribute to the project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License 📄

[Add your license information here]

## Support 🤝

For support, please [create an issue](repository-issues-url) or contact the maintainers. 