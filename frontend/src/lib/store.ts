import { create } from 'zustand';
import { ResumeAnalysisResponse } from '@/types/resume';

interface AnalysisStore {
  analysisResult: ResumeAnalysisResponse | null;
  setAnalysisResult: (result: ResumeAnalysisResponse | null) => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  analysisResult: null,
  setAnalysisResult: (result) => set({ analysisResult: result }),
})); 