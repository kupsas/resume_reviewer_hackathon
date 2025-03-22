# 📊 Data Models Documentation

## Overview
This document outlines the data models used in our Resume Review application, based on the API endpoints we've identified. These models represent the structure of data that flows between our frontend and backend.

## Core Models

### 1. ResumeAnalysisRequest
**Purpose:** Represents the input data for resume analysis
```typescript
/**
 * This interface defines the structure for sending resume text to the backend for analysis.
 * We keep it simple with just two fields to maintain flexibility and ease of use.
 * 
 * Design Decisions:
 * - resume_text is required as it's the core input for analysis
 * - job_description is optional to support both general and job-specific analysis
 * - Using string type for both fields to support any text format
 */
interface ResumeAnalysisRequest {
    resume_text: string;      // Required: The text content of the resume
    job_description?: string; // Optional: Job description to match against
}
```

### 2. ResumeAnalysisResponse
**Purpose:** Represents the complete analysis response from the backend
```typescript
/**
 * This is the main response interface that encapsulates all analysis results.
 * We use a nested structure to organize different aspects of the analysis.
 * 
 * Design Decisions:
 * - status field helps frontend quickly determine if request was successful
 * - resumeAnalysis contains the core analysis results
 * - tokenUsage helps track API costs and usage
 * - jobMatchAnalysis is optional to maintain backward compatibility
 */
interface ResumeAnalysisResponse {
    status: "success" | "error";  // Using union type for strict type checking
    resumeAnalysis: {
        sections: ResumeSection[];
        scores: ResumeScores;
        recommendations: string[];
    };
    tokenUsage: TokenUsage;
    jobMatchAnalysis?: JobMatchAnalysis; // Optional: Only present if job_description was provided
}
```

### 3. ResumeSection
**Purpose:** Represents a section of the resume with its analysis
```typescript
/**
 * This interface represents individual sections of the resume with their analysis.
 * Each section is scored independently to provide granular feedback.
 * 
 * Design Decisions:
 * - name field helps identify different resume sections (Experience, Education, etc.)
 * - content stores the original text for reference
 * - score is a number between 0-1 for consistent scoring across sections
 */
interface ResumeSection {
    name: string;    // e.g., "Experience", "Education"
    content: string; // The actual content of the section
    score: number;   // Score between 0 and 1
}
```

### 4. ResumeScores
**Purpose:** Contains various scoring metrics for the resume
```typescript
/**
 * This interface provides different scoring dimensions for the resume.
 * Multiple scores help provide more nuanced feedback.
 * 
 * Design Decisions:
 * - Each score is a number between 0-1 for consistency
 * - star_format evaluates visual presentation
 * - metrics_usage checks for quantifiable achievements
 * - technical_depth assesses technical content quality
 * - overall provides a weighted average of all scores
 */
interface ResumeScores {
    star_format: number;      // Score for resume formatting
    metrics_usage: number;    // Score for use of quantifiable metrics
    technical_depth: number;  // Score for technical content depth
    overall: number;         // Overall resume score
}
```

### 5. TokenUsage
**Purpose:** Tracks API token consumption and costs
```typescript
/**
 * This interface helps track API usage and costs.
 * Important for monitoring and optimizing API consumption.
 * 
 * Design Decisions:
 * - Separate token counts for different parts of the request
 * - total_cost helps with budget tracking
 * - All fields are numbers for easy calculations
 */
interface TokenUsage {
    total_tokens: number;      // Total tokens used in the request
    prompt_tokens: number;     // Tokens used in the input/prompt
    completion_tokens: number; // Tokens used in the response
    total_cost: number;       // Total cost in USD
}
```

### 6. JobMatchAnalysis
**Purpose:** Contains job matching analysis when a job description is provided
```typescript
/**
 * This interface provides detailed analysis of how well the resume matches a job description.
 * Helps users optimize their resume for specific job applications.
 * 
 * Design Decisions:
 * - match_score provides a quick overall match percentage
 * - skill_matches and missing_skills help identify gaps
 * - recommendations provide actionable feedback
 */
interface JobMatchAnalysis {
    match_score: number;      // Overall match score between resume and job
    skill_matches: string[];  // List of matching skills
    missing_skills: string[]; // List of skills in job but not in resume
    recommendations: string[]; // Specific recommendations for job match
}
```

## Data Transformations

### Frontend to Backend
1. **Text Analysis**
   ```typescript
   /**
    * Text-based analysis uses JSON format for simplicity and readability.
    * This approach is best for:
    * - Simple text submissions
    * - Quick analysis without file handling
    * - Easy debugging and testing
    */
   - Frontend sends raw text in `resume_text` field
   - Optional `job_description` can be included
   - Data is sent as JSON in request body
   ```

2. **File Analysis**
   ```typescript
   /**
    * File uploads use multipart/form-data to handle binary files efficiently.
    * This approach is best for:
    * - PDF and DOCX file uploads
    * - Large file sizes
    * - Maintaining file format integrity
    */
   - Frontend sends file as `multipart/form-data`
   - File must be PDF or DOCX format
   - Optional `job_description` can be included as form field
   ```

### Backend to Frontend
1. **Success Response**
   ```typescript
   /**
    * Success responses follow a consistent structure for easy handling.
    * Benefits:
    * - Clear status indication
    * - Organized data hierarchy
    * - Optional fields for flexibility
    */
   - All responses include `status` field
   - Analysis results are nested under `resumeAnalysis`
   - Token usage statistics are included
   - Job match analysis is optional
   ```

2. **Error Response**
   ```typescript
   /**
    * Error responses provide detailed information for debugging.
    * Design ensures:
    * - Clear error identification
    * - Detailed error messages
    * - Consistent structure with success responses
    */
   - Includes `status: "error"`
   - Contains `detail` field with error message
   - May include `code` field for specific error types
   - Empty `tokenUsage` object included
   ```

## Data Validation Rules

### Input Validation
1. `resume_text`
   ```typescript
   /**
    * Resume text validation ensures:
    * - Required field presence
    * - Non-empty content
    * - Reasonable length limits (TBD based on API constraints)
    */
   - Required field
   - Must be non-empty string
   - Maximum length: TBD (to be determined)
   ```

2. `job_description`
   ```typescript
   /**
    * Job description validation:
    * - Optional field for flexibility
    * - String type for consistency
    * - Length limits to be determined
    */
   - Optional field
   - Must be string if provided
   - Maximum length: TBD
   ```

3. File Upload
   ```typescript
   /**
    * File upload validation ensures:
    * - Supported file formats only
    * - Reasonable file size limits
    * - Secure file handling
    */
   - Must be PDF or DOCX format
   - Maximum file size: TBD
   ```

### Output Validation
1. Scores
   ```typescript
   /**
    * Score validation ensures:
    * - Consistent range (0-1)
    * - Numeric type for calculations
    * - Reliable comparison operations
    */
   - All scores must be between 0 and 1
   - Must be numbers (not strings)
   ```

2. Arrays
   ```typescript
   /**
    * Array validation ensures:
    * - Correct data types
    * - Valid object structures
    * - Consistent data format
    */
   - `recommendations` must be array of strings
   - `sections` must be array of valid ResumeSection objects
   ```

## Next Steps
- [ ] Determine maximum lengths for text fields
- [ ] Set file size limits for uploads
- [ ] Add validation rules for specific fields
- [ ] Create TypeScript interfaces for frontend use
- [ ] Add example data for each model
- [ ] Document any data transformation requirements

## 🔄 Updates
- Initial documentation created based on API endpoints
- Added detailed interface definitions
- Included validation rules
- Documented data transformation requirements
- Added comprehensive rationales for all models and validation rules 