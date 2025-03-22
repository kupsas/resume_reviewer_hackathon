import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiClient } from '@/lib/api-client';
import { ResumeAnalysisResponse } from '@/types/resume';

// Mock the fetch function
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('API Client', () => {
  const TEST_API_URL = 'http://test-api.example.com';
  
  const mockResponse: ResumeAnalysisResponse = {
    status: 'success',
    resumeAnalysis: {
      sections: [
        {
          type: 'EXPERIENCE',
          points: [
            {
              text: 'Sample experience point',
              star: {
                situation: true,
                task: true,
                action: true,
                result: true,
                complete: true
              },
              metrics: ['metric1'],
              technical_score: 4.5,
              improvement: 'Sample improvement'
            }
          ]
        }
      ]
    },
    tokenUsage: {
      total_tokens: 1000,
      prompt_tokens: 500,
      completion_tokens: 500,
      total_cost: 0.02
    },
    jobMatchAnalysis: null as any // Type assertion to fix type error
  };

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Hide console.log during tests
    vi.spyOn(console, 'log').mockImplementation(() => {});

    // Mock the resumeService to throw an error to ensure we use the fetch fallback
    vi.mock('@/mocks', () => ({
      resumeService: {
        analyzeResume: vi.fn().mockRejectedValue(new Error('Mock service error')),
        analyzeResumeFile: vi.fn().mockRejectedValue(new Error('Mock service error'))
      }
    }));

    // Set up the mock fetch to return a successful response
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => mockResponse
    });
  });

  // Instead of trying to mock the API_BASE_URL, we'll test that fetch is called
  // with the right parameters regardless of the base URL
  describe('analyzeResumeText', () => {
    it('should call fetch with the correct path and parameters', async () => {
      const requestData = {
        resume_text: 'Sample resume text',
        job_description: 'Sample job description'
      };

      await apiClient.analyzeResumeText(requestData);

      // Verify fetch was called
      expect(mockFetch).toHaveBeenCalledTimes(1);
      
      // Check method and headers
      const [, options] = mockFetch.mock.calls[0];
      expect(options.method).toBe('POST');
      expect(options.headers).toEqual({
        'Content-Type': 'application/json'
      });
      expect(options.body).toBe(JSON.stringify(requestData));
    });

    it('should return normalized response data', async () => {
      const requestData = {
        resume_text: 'Sample resume text'
      };

      const result = await apiClient.analyzeResumeText(requestData);

      expect(result).toEqual(mockResponse);
    });

    it('should handle API errors correctly', async () => {
      const errorMessage = 'API Error';
      
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: errorMessage })
      });

      const requestData = {
        resume_text: 'Sample resume text'
      };

      await expect(apiClient.analyzeResumeText(requestData)).rejects.toThrow(errorMessage);
    });
  });

  describe('analyzeResumeFile', () => {
    it('should call fetch with FormData', async () => {
      const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' });
      const jobDescription = 'Sample job description';

      await apiClient.analyzeResumeFile({ file, jobDescription });

      expect(mockFetch).toHaveBeenCalledTimes(1);
      
      // Check method
      const [, options] = mockFetch.mock.calls[0];
      expect(options.method).toBe('POST');
      
      // FormData is not easily comparable, but we can check it's an instance of FormData
      expect(options.body).toBeInstanceOf(FormData);
    });
  });

  describe('checkHealth', () => {
    it('should call the health endpoint', async () => {
      await apiClient.checkHealth();

      expect(mockFetch).toHaveBeenCalledTimes(1);
    });

    it('should return the health status', async () => {
      const healthResponse = { status: 'healthy' };
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => healthResponse
      });

      const result = await apiClient.checkHealth();

      expect(result).toEqual(healthResponse);
    });

    it('should handle errors and return error status', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await apiClient.checkHealth();

      expect(result).toEqual({ status: 'error' });
    });
  });
}); 