export interface StarAnalysis {
  situation: boolean;
  task: boolean;
  action: boolean;
  result: boolean;
  complete: boolean;
}

export interface BulletPointAnalysis {
  text: string;
  star: StarAnalysis;
  metrics: string[];
  improvement: string;
  technicalScore: number;
}

export interface JobMatch {
  match_score: number;
  technical_match: {
    matched_skills: string[];
    missing_skills: string[];
    skill_coverage_score: number;
  };
  experience_match: {
    required_years: number;
    actual_years: number;
    experience_score: number;
  };
  key_requirements: {
    met: string[];
    partially_met: string[];
    not_met: string[];
  };
  recommendations: string[];
}

export interface ResumeAnalysisResponse {
  bulletPoints: BulletPointAnalysis[];
  jobMatch: JobMatch;
  overallScore: number;
} 