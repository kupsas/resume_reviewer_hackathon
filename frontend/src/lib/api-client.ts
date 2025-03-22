import { useMutation } from '@tanstack/react-query';
import { ResumeAnalysisRequest, ResumeAnalysisResponse } from '@/types/resume';
import { resumeService } from '@/mocks';
import { config, isDevelopment } from './config';

// API base URL configuration
const API_BASE_URL = config.API_BASE_URL;

// Log only in development mode
if (isDevelopment()) {
  console.log('API Base URL:', API_BASE_URL);
}

// Helper function to handle API errors
const handleApiError = async (response: Response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An unknown error occurred' }));
    console.error('API Error:', error);
    throw new Error(error.detail || 'An error occurred while processing your request');
  }
  return response.json();
};

// Helper function to normalize API response
const normalizeResponse = (data: any): ResumeAnalysisResponse => {
  // Log the response structure for debugging in development
  if (isDevelopment()) {
    console.log('API Response structure:', JSON.stringify(data, null, 2));
  }
  
  // Ensure the response matches our expected format
  if (!data || typeof data !== 'object') {
    throw new Error('Invalid response format');
  }
  
  return {
    status: data.status || 'error',
    resumeAnalysis: data.resumeAnalysis || { sections: [] },
    tokenUsage: data.tokenUsage || { 
      total_tokens: 0, 
      prompt_tokens: 0, 
      completion_tokens: 0, 
      total_cost: 0 
    },
    jobMatchAnalysis: data.jobMatchAnalysis || null
  };
};

interface FileAnalysisParams {
  file: File;
  jobDescription?: string;
}

// API client functions
export const apiClient = {
  // Text-based resume analysis
  analyzeResumeText: async (data: ResumeAnalysisRequest): Promise<ResumeAnalysisResponse> => {
    console.log('Making API call to:', `${API_BASE_URL}/api/resume/analyze`); // Debug log
    
    try {
      // Try using the mock service if available
      return await resumeService.analyzeResume(data.resume_text, data.job_description);
    } catch (error) {
      console.log('Mock service not available or error, using real API');
      // Fallback to real API
      const response = await fetch(`${API_BASE_URL}/api/resume/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const responseData = await handleApiError(response);
      return normalizeResponse(responseData);
    }
  },

  // File-based resume analysis
  analyzeResumeFile: async (params: FileAnalysisParams): Promise<ResumeAnalysisResponse> => {
    console.log('Making API call to:', `${API_BASE_URL}/api/resume/analyze/file`); // Debug log
    
    try {
      // Try using the mock service if available
      return await resumeService.analyzeResumeFile(params.file, params.jobDescription);
    } catch (error) {
      console.log('Mock service not available or error, using real API');
      // Fallback to real API
      const formData = new FormData();
      formData.append('file', params.file);
      if (params.jobDescription) {
        formData.append('job_description', params.jobDescription);
      }

      const response = await fetch(`${API_BASE_URL}/api/resume/analyze/file`, {
        method: 'POST',
        body: formData,
      });
      const responseData = await handleApiError(response);
      return normalizeResponse(responseData);
    }
  },

  // Health check
  checkHealth: async (): Promise<{ status: string }> => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return handleApiError(response);
    } catch (error) {
      console.error('Health check error:', error);
      return { status: 'error' };
    }
  },
};

// React Query hooks
export const useResumeAnalysis = () => {
  return useMutation({
    mutationFn: apiClient.analyzeResumeText,
    onError: (error) => {
      console.error('Resume analysis error:', error);
    },
  });
};

export const useResumeFileAnalysis = () => {
  return useMutation({
    mutationFn: apiClient.analyzeResumeFile,
    onError: (error) => {
      console.error('Resume file analysis error:', error);
    },
  });
}; 