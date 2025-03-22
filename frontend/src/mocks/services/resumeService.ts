import { mockResumeData } from '../data/resumeData';

/**
 * A mock service that simulates the backend API for resume analysis.
 * Use this for UI component development when the actual backend is not available.
 */
export class MockResumeService {
  /**
   * Simulates analyzing a resume text
   * @param resumeText The text content of the resume
   * @param jobDescription Optional job description to match against
   * @returns A promise resolving to the analysis result
   */
  static async analyzeResume(resumeText: string, jobDescription?: string): Promise<any> {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Return mock data
    return mockResumeData;
  }

  /**
   * Simulates analyzing a resume file
   * @param file The resume file (PDF or DOCX)
   * @param jobDescription Optional job description to match against
   * @returns A promise resolving to the analysis result
   */
  static async analyzeResumeFile(file: File, jobDescription?: string): Promise<any> {
    // Check file type
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    
    if (fileExtension !== 'pdf' && fileExtension !== 'docx') {
      throw new Error('Unsupported file type. Please upload a PDF or DOCX file.');
    }
    
    // Simulate file upload and processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Return mock data
    return mockResumeData;
  }
}

/**
 * Constants for API endpoints
 * Use these when you're ready to switch from mock to real API
 */
export const API_ENDPOINTS = {
  ANALYZE_RESUME: '/api/resume/analyze',
  ANALYZE_RESUME_FILE: '/api/resume/analyze/file'
}; 