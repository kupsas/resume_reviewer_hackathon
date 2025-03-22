import { MockResumeService, API_ENDPOINTS } from './services/resumeService';
import { mockResumeData } from './data/resumeData';

// Configuration for using mocks
const USE_MOCKS = true;

/**
 * Resume service that automatically switches between mock and real implementation
 * based on the USE_MOCKS configuration
 */
export const resumeService = {
  analyzeResume: async (resumeText: string, jobDescription?: string): Promise<any> => {
    if (USE_MOCKS) {
      return MockResumeService.analyzeResume(resumeText, jobDescription);
    } else {
      // Implementation using real API
      const response = await fetch(API_ENDPOINTS.ANALYZE_RESUME, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return response.json();
    }
  },

  analyzeResumeFile: async (file: File, jobDescription?: string): Promise<any> => {
    if (USE_MOCKS) {
      return MockResumeService.analyzeResumeFile(file, jobDescription);
    } else {
      // Implementation using real API
      const formData = new FormData();
      formData.append('file', file);
      
      if (jobDescription) {
        formData.append('job_description', jobDescription);
      }

      const response = await fetch(API_ENDPOINTS.ANALYZE_RESUME_FILE, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return response.json();
    }
  }
};

// Export everything for direct use if needed
export {
  mockResumeData,
  MockResumeService,
  API_ENDPOINTS,
}; 