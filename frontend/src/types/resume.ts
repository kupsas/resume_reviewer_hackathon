// Request Types
export interface ResumeAnalysisRequest {
    resume_text: string;
    job_description?: string;
}

// Response Types

// New interfaces for education points
export interface EducationReputation {
    domestic_score: number;
    domestic_score_rationale: string;
    international_score: number;
    international_score_rationale: string;
}

export interface EducationPoint {
    text: string;
    subject: string;
    course: string;
    school: string;
    subject_course_school_reputation: EducationReputation;
    improvement?: string; // Optional for backward compatibility
}

// Base interface for common properties
export interface BaseResumePoint {
    text: string;
    improvement: string;
}

// Standard resume point (for experience/projects)
export interface StandardResumePoint extends BaseResumePoint {
    star: {
        situation: boolean;
        task: boolean;
        action: boolean;
        result: boolean;
        complete: boolean;
    };
    metrics: string[];
    technical_score: number;
}

// Discriminated union type for all resume points
export type ResumePoint = StandardResumePoint | EducationPoint;

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