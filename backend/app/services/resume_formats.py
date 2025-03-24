# Resume point extraction format
POINT_EXTRACTION_FORMAT = {
    "points": [
        {
            "id": "leave_empty",
            "text": "bullet point text",
            "section": "section name",
            "company": "company name if applicable",
            "dates": {
                "startDate": "YYYY-MM",
                "endDate": "YYYY-MM or Present"
            }
        }
    ]
}

# Resume analysis format
RESUME_ANALYSIS_FORMAT = {
    "resumeAnalysis": {
        "points": [
            {
                "id": "point_id",
                "text": "bullet text",
                "section": "section name",
                "analysis": {
                    "star": {
                        "complete": "boolean",
                        "missing": ["missing components"]
                    },
                    "metrics": ["identified metrics"],
                    "contribution": "1-5 score"
                },
                "improvement": "suggested improvement"
            }
        ],
        "overall": {
            "starScore": "1-5",
            "metricsScore": "1-5",
            "contributionScore": "1-5",
            "recommendations": [
                {
                    "priority": "high/medium/low",
                    "action": "what to do"
                }
            ]
        }
    }
}

# Job match analysis format
JOB_MATCH_FORMAT = {
    "jobMatchAnalysis": {
        "skills": {
            "matched": ["matched skills"],
            "missing": ["missing skills"],
            "score": "percentage"
        },
        "experience": {
            "relevantYears": "number",
            "score": "percentage",
            "gaps": ["identified gaps"]
        },
        "leadership": {
            "score": "percentage",
            "examples": ["leadership examples"]
        },
        "recommendations": ["general improvement recommendations"]
    }
}

# Integrated improvements format
INTEGRATED_IMPROVEMENTS_FORMAT = {
    "integratedImprovements": {
        "points": [
            {
                "id": "point_id_from_input",
                "originalText": "original text",
                "generalImprovement": "improved version from resume analysis",
                "jobTailoredImprovement": "improved version from job match if available, empty string if no job description",
                "combinedBestVersion": "best version combining both improvements",
                "improvementSummary": {
                    "resumeIssuesSolved": [
                        "list of resume issues addressed"
                    ],
                    "jobAlignmentImprovements": [
                        "list of job alignment improvements if job description provided, empty list if not"
                    ]
                }
            }
        ]
    }
} 