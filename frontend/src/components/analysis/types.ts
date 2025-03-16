export interface CategoryScore {
  name: string;
  score: number;
  maxScore: number;
  percentage: number;
  displayName?: string;
}

export interface Analysis {
  status: string;
  analysis: string;
} 