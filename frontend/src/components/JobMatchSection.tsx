import React from 'react';
import { cn } from '@/lib/utils';
import { Check, AlertCircle, X, Clock, Award } from 'lucide-react';
import ScoreCard from './ScoreCard';
import { JobMatchAnalysis } from '@/types/resume';

interface JobMatchSectionProps {
  matchData: JobMatchAnalysis;
  className?: string;
}

const JobMatchSection: React.FC<JobMatchSectionProps> = ({ matchData, className }) => {
  // Handle potentially missing data with defaults
  const matchScore = matchData?.match_score ?? 0;
  
  const technicalMatch = matchData?.technical_match ?? {
    matched_skills: [],
    missing_skills: [],
    skill_coverage_score: 0
  };
  
  const experienceMatch = matchData?.experience_match ?? {
    required_years: 0,
    actual_years: 0,
    experience_score: 0
  };
  
  // Calculate experience score - 100% if actual years >= required years
  const displayExperienceScore = experienceMatch.actual_years >= experienceMatch.required_years ? 100 : experienceMatch.experience_score;
  
  const keyRequirements = matchData?.key_requirements ?? {
    met: [],
    partially_met: [],
    not_met: []
  };
  
  const recommendations = matchData?.recommendations ?? [];

  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="p-5 border-b">
        <h3 className="font-semibold text-lg">Job Match Analysis</h3>
      </div>
      
      <div className="p-5 space-y-8">
        {/* Score cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <ScoreCard 
            title="Overall Match" 
            score={matchScore}
            description="How well your resume matches the job requirements"
          />
          <ScoreCard 
            title="Skills Coverage" 
            score={technicalMatch.skill_coverage_score}
            description="How many of the required skills your resume covers"
          />
        </div>
        
        {/* Experience Match and Skills Analysis sections */}
        <div className="mb-12">  {/* Increased margin bottom for better separation */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Experience Match Section */}
            <div className="lg:col-span-1">
              <h4 className="font-medium mb-4">Experience Match</h4>
              <div className="bg-card border rounded-lg p-6">  {/* Increased padding */}
                <div className="space-y-4">  {/* Increased spacing between items */}
                  <div className="flex items-center gap-3">
                    <Clock className="h-5 w-5 text-primary" />
                    <span className="font-medium">Required Years: {experienceMatch.required_years}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Award className="h-5 w-5 text-success" />
                    <span className="font-medium">Your Experience: {experienceMatch.actual_years} years</span>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Skills section */}
            <div className="lg:col-span-2">
              <h4 className="font-medium mb-4">Skills Analysis</h4>
              <div className="bg-card border rounded-lg p-6">  {/* Increased padding */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                      <Check className="h-4 w-4 text-success" />
                      <span>Matched Skills</span>
                    </h5>
                    {technicalMatch.matched_skills.length > 0 ? (
                      <div className="flex flex-wrap gap-2">
                        {technicalMatch.matched_skills.map((skill, index) => (
                          <span key={index} className="chip bg-success/10 text-success border border-success/20">
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">No matched skills found</p>
                    )}
                  </div>
                  
                  <div className="space-y-2">
                    <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                      <X className="h-4 w-4 text-destructive" />
                      <span>Missing Skills</span>
                    </h5>
                    {technicalMatch.missing_skills.length > 0 ? (
                      <div className="flex flex-wrap gap-2">
                        {technicalMatch.missing_skills.map((skill, index) => (
                          <span key={index} className="chip bg-destructive/10 text-destructive border border-destructive/20">
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted-foreground">No missing skills found</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Requirements section */}
        <div>
          <h4 className="font-medium mb-6">Key Requirements</h4>  {/* Increased bottom margin */}
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">  {/* Increased gap */}
            {/* Met requirements */}
            <div className="bg-card border rounded-lg p-6">  {/* Made into a card */}
              <h5 className="text-sm font-medium text-success flex items-center gap-2 mb-4">
                <Check className="h-5 w-5" />
                <span>Met Requirements</span>
              </h5>
              {keyRequirements.met.length > 0 ? (
                <div className="space-y-3">  {/* Increased spacing between items */}
                  {keyRequirements.met.map((req, index) => (
                    <div key={index} className="flex items-start gap-2 bg-success/5 border border-success/10 rounded-lg p-3">
                      <Check className="h-4 w-4 text-success mt-0.5 flex-shrink-0" />
                      <p className="text-sm">{req}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">No met requirements found</p>
              )}
            </div>
            
            {/* Partially met requirements */}
            <div className="bg-card border rounded-lg p-6">  {/* Made into a card */}
              <h5 className="text-sm font-medium text-warning flex items-center gap-2 mb-4">
                <Clock className="h-5 w-5" />
                <span>Partially Met Requirements</span>
              </h5>
              {keyRequirements.partially_met.length > 0 ? (
                <div className="space-y-3">  {/* Increased spacing between items */}
                  {keyRequirements.partially_met.map((req, index) => (
                    <div key={index} className="flex items-start gap-2 bg-warning/5 border border-warning/10 rounded-lg p-3">
                      <Clock className="h-4 w-4 text-warning mt-0.5 flex-shrink-0" />
                      <p className="text-sm">{req}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">No partially met requirements found</p>
              )}
            </div>
            
            {/* Not met requirements */}
            <div className="bg-card border rounded-lg p-6">  {/* Made into a card */}
              <h5 className="text-sm font-medium text-destructive flex items-center gap-2 mb-4">
                <X className="h-5 w-5" />
                <span>Not Met Requirements</span>
              </h5>
              {keyRequirements.not_met.length > 0 ? (
                <div className="space-y-3">  {/* Increased spacing between items */}
                  {keyRequirements.not_met.map((req, index) => (
                    <div key={index} className="flex items-start gap-2 bg-destructive/5 border border-destructive/10 rounded-lg p-3">
                      <X className="h-4 w-4 text-destructive mt-0.5 flex-shrink-0" />
                      <p className="text-sm">{req}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">No unmet requirements found</p>
              )}
            </div>
            
            {/* Show message if no requirements are found */}
            {keyRequirements.met.length === 0 && 
             keyRequirements.partially_met.length === 0 && 
             keyRequirements.not_met.length === 0 && (
              <div className="col-span-3 flex items-center justify-center py-4">
                <p className="text-sm text-muted-foreground">No key requirements analysis available</p>
              </div>
            )}
          </div>
        </div>
        
        {/* Recommendations section */}
        <div className="space-y-4">
          <h4 className="font-medium">Recommendations</h4>
          {recommendations.length > 0 ? (
            <div className="space-y-2">
              {recommendations.map((recommendation, index) => (
                <div key={index} className="flex items-start gap-2">
                  <AlertCircle className="h-5 w-5 text-warning mt-0.5" />
                  <p className="text-sm">{recommendation}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No recommendations available</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobMatchSection;
