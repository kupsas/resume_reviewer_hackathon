import React from 'react';
import { cn } from '@/lib/utils';
import { Check, AlertCircle, X } from 'lucide-react';
import ScoreCard from './ScoreCard';

interface JobMatchSectionProps {
  jobMatchAnalysis: {
    match_score: number;
    key_skills_match: Array<{
      skill: string;
      present: boolean;
      importance: string;
    }>;
    missing_skills: string[];
    recommendations: string[];
  };
  className?: string;
}

const JobMatchSection: React.FC<JobMatchSectionProps> = ({ jobMatchAnalysis, className }) => {
  // Early return if jobMatchAnalysis is not provided or incomplete
  if (!jobMatchAnalysis || !jobMatchAnalysis.match_score) {
    return (
      <div className={cn("rounded-xl border bg-card p-5", className)}>
        <div className="text-center p-8">
          <h3 className="font-semibold text-lg mb-2">Job Match Data Not Available</h3>
          <p className="text-muted-foreground">Please upload a resume and job description to view match analysis.</p>
        </div>
      </div>
    );
  }

  // Extract matched and missing skills
  const matchedSkills = jobMatchAnalysis.key_skills_match
    .filter(skill => skill.present)
    .map(skill => skill.skill);
  
  const missingSkills = jobMatchAnalysis.missing_skills || [];

  // Mock data for experience section
  const experienceData = {
    required_years: 3,
    actual_years: 5,
    experience_score: 1.0
  };

  // Mock data for key requirements section
  const keyRequirements = {
    met: [
      "3+ years of experience in software development",
      "Proficiency in Python, JavaScript",
      "Experience with SQL and NoSQL databases",
      "Version control with Git",
      "Experience with cloud platforms (AWS, GCP)",
      "Knowledge of microservices architecture",
      "Understanding of CI/CD practices"
    ],
    partially_met: [
      "Experience with web frameworks (Django, Flask, or FastAPI)",
      "Experience with machine learning or AI technologies"
    ],
    not_met: [
      "Experience with React/Next.js",
      "Contributions to open-source projects"
    ]
  };

  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="p-5 border-b">
        <h3 className="font-semibold text-lg">Job Match Analysis</h3>
      </div>
      
      <div className="p-5 space-y-6">
        {/* Score cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <ScoreCard 
            title="Overall Match" 
            score={Math.round(jobMatchAnalysis.match_score * 100)}
            description="How well your resume matches the job requirements"
          />
          <ScoreCard 
            title="Experience" 
            score={100}
            description={`Required: ${experienceData.required_years} years, You have: ${experienceData.actual_years} years`}
          />
        </div>
        
        {/* Skills section */}
        <div className="space-y-4">
          <h4 className="font-medium">Skills Analysis</h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                <Check className="h-4 w-4 text-success" />
                <span>Matched Skills</span>
              </h5>
              <div className="flex flex-wrap gap-2">
                {matchedSkills.map((skill, index) => (
                  <span key={index} className="chip bg-success/10 text-success border border-success/20 px-2 py-1 rounded-full text-xs">
                    {skill}
                  </span>
                ))}
                {matchedSkills.length === 0 && (
                  <span className="text-sm text-muted-foreground">No matched skills found</span>
                )}
              </div>
            </div>
            
            <div className="space-y-2">
              <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                <X className="h-4 w-4 text-destructive" />
                <span>Missing Skills</span>
              </h5>
              <div className="flex flex-wrap gap-2">
                {missingSkills.map((skill, index) => (
                  <span key={index} className="chip bg-destructive/10 text-destructive border border-destructive/20 px-2 py-1 rounded-full text-xs">
                    {skill}
                  </span>
                ))}
                {missingSkills.length === 0 && (
                  <span className="text-sm text-muted-foreground">No missing skills found</span>
                )}
              </div>
            </div>
          </div>
        </div>
        
        {/* Requirements section */}
        <div className="space-y-4">
          <h4 className="font-medium">Key Requirements</h4>
          
          <div className="space-y-4">
            {keyRequirements.met.length > 0 && (
              <div className="space-y-2">
                <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <Check className="h-4 w-4 text-success" />
                  <span>Requirements Met</span>
                </h5>
                <ul className="space-y-1">
                  {keyRequirements.met.map((req, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <Check className="h-4 w-4 text-success shrink-0 mt-1" />
                      <span className="text-sm">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {keyRequirements.partially_met.length > 0 && (
              <div className="space-y-2">
                <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <AlertCircle className="h-4 w-4 text-warning" />
                  <span>Partially Met</span>
                </h5>
                <ul className="space-y-1">
                  {keyRequirements.partially_met.map((req, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <AlertCircle className="h-4 w-4 text-warning shrink-0 mt-1" />
                      <span className="text-sm">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {keyRequirements.not_met.length > 0 && (
              <div className="space-y-2">
                <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <X className="h-4 w-4 text-destructive" />
                  <span>Not Met</span>
                </h5>
                <ul className="space-y-1">
                  {keyRequirements.not_met.map((req, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <X className="h-4 w-4 text-destructive shrink-0 mt-1" />
                      <span className="text-sm">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        
        {/* Recommendations */}
        {jobMatchAnalysis.recommendations && jobMatchAnalysis.recommendations.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium">Recommendations</h4>
            <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
              <ul className="space-y-2">
                {jobMatchAnalysis.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <div className="h-5 w-5 rounded-full bg-primary/20 text-primary flex items-center justify-center shrink-0 mt-0.5">
                      <span className="text-xs font-bold">{index + 1}</span>
                    </div>
                    <span className="text-sm">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobMatchSection;
