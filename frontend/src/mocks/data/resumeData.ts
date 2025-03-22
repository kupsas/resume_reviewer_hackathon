export const mockResumeData = {
  "status": "success",
  "resumeAnalysis": {
    "sections": [
      {
        "type": "Experience",
        "points": [
          {
            "text": "Led development of cloud-based microservices architecture, improving system reliability by 99.9%",
            "star": {
              "situation": true,
              "task": true,
              "action": true,
              "result": true,
              "complete": true
            },
            "metrics": [
              "99.9%"
            ],
            "technical_score": 5,
            "improvement": "Led the development of a cloud-based microservices architecture, resulting in a 99.9% improvement in system reliability."
          },
          {
            "text": "Implemented AI-powered recommendation engine, increasing user engagement by 45%",
            "star": {
              "situation": true,
              "task": true,
              "action": true,
              "result": true,
              "complete": true
            },
            "metrics": [
              "45%"
            ],
            "technical_score": 5,
            "improvement": "Implemented an AI-powered recommendation engine that increased user engagement by 45%."
          },
          {
            "text": "Mentored junior developers and conducted code reviews for team of 8 engineers",
            "star": {
              "situation": true,
              "task": true,
              "action": true,
              "result": false,
              "complete": false
            },
            "metrics": [
              "8 engineers"
            ],
            "technical_score": 3,
            "improvement": "Mentored junior developers and conducted code reviews for a team of 8 engineers, resulting in a 30% reduction in bugs found in production."
          }
        ],
        "analysis": "Your experience section effectively demonstrates your technical skills and leadership abilities. Most bullet points follow the STAR format well, though a few could be improved by adding more specific results."
      },
      {
        "type": "Skills",
        "points": [
          {
            "text": "Programming Languages: Python, JavaScript, TypeScript, Java, C++",
            "technical_score": 4,
            "improvement": ""
          },
          {
            "text": "Frameworks: React, Angular, Node.js, Django, Flask",
            "technical_score": 4,
            "improvement": ""
          },
          {
            "text": "Tools: Docker, Kubernetes, AWS, GCP, CI/CD pipelines",
            "technical_score": 5,
            "improvement": ""
          }
        ],
        "analysis": "Your skills section is comprehensive and shows a strong technical foundation. Consider organizing skills by proficiency level or relevance to target roles."
      },
      {
        "type": "Education",
        "points": [
          {
            "text": "M.S. Computer Science, Stanford University, 2018-2020",
            "technical_score": 5,
            "improvement": ""
          },
          {
            "text": "B.S. Computer Engineering, UC Berkeley, 2014-2018",
            "technical_score": 4,
            "improvement": ""
          }
        ],
        "analysis": "Your education section is clear and concise. Consider adding relevant coursework or academic achievements to strengthen this section."
      }
    ],
    "scores": {
      "star_format": 0.85,
      "metrics_usage": 0.90,
      "technical_depth": 0.95,
      "overall": 0.90
    },
    "recommendations": [
      "Add more quantifiable results to your experience bullet points",
      "Consider grouping your skills by proficiency level",
      "Add relevant coursework to your education section",
      "Ensure all experience points follow the complete STAR format"
    ]
  },
  "tokenUsage": {
    "total_tokens": 1250,
    "prompt_tokens": 750,
    "completion_tokens": 500,
    "total_cost": 0.025
  },
  "jobMatchAnalysis": {
    "match_score": 0.82,
    "key_skills_match": [
      {
        "skill": "React",
        "present": true,
        "importance": "high"
      },
      {
        "skill": "AWS",
        "present": true,
        "importance": "high"
      },
      {
        "skill": "Python",
        "present": true,
        "importance": "medium"
      },
      {
        "skill": "GraphQL",
        "present": false,
        "importance": "medium"
      }
    ],
    "missing_skills": [
      "GraphQL",
      "Redux",
      "PostgreSQL"
    ],
    "recommendations": [
      "Add experience with GraphQL to your resume if applicable",
      "Highlight your React experience more prominently",
      "Consider mentioning database experience specifically"
    ]
  }
}; 