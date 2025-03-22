import { useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { ResumeAnalysisResponse } from '@/types/resume';
import { useToast } from '@/hooks/use-toast';
import { useAnalysisStore } from '@/lib/store';

interface FileAnalysisParams {
  file: File;
  jobDescription?: string;
}

interface UseResumeAnalysisReturn {
  loading: boolean;
  error: Error | null;
  analyzeResume: (file: File, jobDescription?: string) => Promise<void>;
  analyzeResumeText: (resumeText: string, jobDescription?: string) => Promise<void>;
  analysisResult: ResumeAnalysisResponse | null;
}

export const useResumeAnalysis = (): UseResumeAnalysisReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const setAnalysisResult = useAnalysisStore(state => state.setAnalysisResult);
  const analysisResult = useAnalysisStore(state => state.analysisResult);
  const { toast } = useToast();

  const analyzeResume = async (file: File, jobDescription?: string) => {
    try {
      setLoading(true);
      setError(null);
      console.log('Starting file analysis...', { file, jobDescription });
      const result = await apiClient.analyzeResumeFile({ file, jobDescription });
      console.log('File analysis complete:', result);
      setAnalysisResult(result);
      toast({
        title: "Analysis Complete! 🎉",
        description: "Your resume has been successfully analyzed.",
      });
    } catch (error) {
      console.error('Resume analysis error:', error);
      setError(error instanceof Error ? error : new Error('An error occurred'));
      toast({
        title: "Analysis Failed 😢",
        description: error instanceof Error ? error.message : "An error occurred while analyzing your resume.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const analyzeResumeText = async (resumeText: string, jobDescription?: string) => {
    try {
      setLoading(true);
      setError(null);
      console.log('Starting text analysis...', { resumeText, jobDescription });
      const result = await apiClient.analyzeResumeText({ resume_text: resumeText, job_description: jobDescription });
      console.log('Text analysis complete:', result);
      setAnalysisResult(result);
      toast({
        title: "Analysis Complete! 🎉",
        description: "Your resume has been successfully analyzed.",
      });
    } catch (error) {
      console.error('Resume analysis error:', error);
      setError(error instanceof Error ? error : new Error('An error occurred'));
      toast({
        title: "Analysis Failed 😢",
        description: error instanceof Error ? error.message : "An error occurred while analyzing your resume.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    analyzeResume,
    analyzeResumeText,
    analysisResult,
  };
}; 