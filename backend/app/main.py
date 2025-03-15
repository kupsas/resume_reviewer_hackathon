from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import resume

app = FastAPI(
    title="Resume Reviewer API",
    description="API for analyzing and providing feedback on resumes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["resume"])

@app.get("/")
async def root():
    return {"message": "Welcome to Resume Reviewer API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 