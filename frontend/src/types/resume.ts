// Request Types
export interface ResumeAnalysisRequest {
    resume_text: string;
    job_description?: string;
}

// Response Types
export interface ResumePoint {
    text: string;
    star: {
        situation: boolean;
        task: boolean;
        action: boolean;
        result: boolean;
        complete: boolean;
    };
    metrics: string[];
    technical_score: number;
    improvement: string;
}

export interface ResumeSection {
    type: string;
    points: ResumePoint[];
}

export interface ResumeScores {
    star_format: number;
    metrics_usage: number;
    technical_depth: number;
    overall: number;
}

export interface TokenUsage {
    total_tokens: number;
    prompt_tokens: number;
    completion_tokens: number;
    total_cost: number;
}

export interface JobMatchAnalysis {
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
    section_recommendations: {
        experience_projects: {
            original_point: string;
            improved_version: string;
        }[];
        education: string;
        skills_certs: string;
    };
    recommendations: string[];
}

export interface ResumeAnalysisResponse {
    status: "success" | "error";
    resumeAnalysis: {
        sections: ResumeSection[];
        recommendations?: string[];
    };
    tokenUsage: TokenUsage;
    jobMatchAnalysis?: JobMatchAnalysis;
} 