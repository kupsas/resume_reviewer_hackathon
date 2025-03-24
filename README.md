# 📄 Resume Reviewer

A comprehensive web application that helps job seekers improve their resumes through AI-powered analysis and feedback.

## ✨ Features

- 📁 Upload resume in PDF or DOCX format
- ✏️ Paste job description text directly
- 🔍 Get detailed section-by-section analysis
- 💼 Match resume against job descriptions
- 🚀 Receive actionable improvement suggestions
- 📊 Score your resume against various criteria
- 🛠️ Responsive modern UI built with React and Tailwind

## 🛠️ Technology Stack

### Backend
- FastAPI - Python-based web framework
- OpenAI API - For AI-powered resume analysis
- PDF and DOCX parsing libraries
- Pydantic for data validation
- Uvicorn for ASGI server

### Frontend
- React with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Shadcn UI component library
- React Router for navigation
- React Query for data fetching
- Framer Motion for animations

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key

## 🚀 Installation

### Clone the repository
```bash
git clone https://github.com/kupsas/resume_reviewer_hackathon
cd resume-reviewer
```

### Backend Setup
```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Start the backend server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## 🔧 Usage

1. Open your browser and navigate to the frontend URL (typically http://localhost:5173 or http://localhost:3000 )
2. Upload your resume (PDF or DOCX) or paste your resume text
3. Optionally paste a job description for targeted feedback
4. Click "Analyze Resume" and wait for the analysis to complete
5. Review the detailed feedback and suggestions

## 📝 API Endpoints

- `POST /api/resume/analyze` - Analyze resume text
- `POST /api/resume/analyze/file` - Analyze resume file (PDF/DOCX)
- `GET /health` - Health check endpoint

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Backend
The backend is deployed on Railway. Follow these steps to deploy:

1. Create a new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Set up the required environment variables in Railway dashboard
4. Railway will automatically deploy your application

### Frontend
The frontend is deployed on Vercel. Follow these steps to deploy:

1. Push your code to GitHub
2. Import your repository on [Vercel](https://vercel.com)
3. Configure your project settings
4. Vercel will automatically build and deploy your application

The built static files will be in the `dist` directory, which can be deployed to any static hosting service like Netlify, Vercel, or GitHub Pages.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
