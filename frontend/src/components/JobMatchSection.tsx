
import React from 'react';
import { cn } from '@/lib/utils';
import { Check, AlertCircle, X } from 'lucide-react';
import ScoreCard from './ScoreCard';

interface JobMatchSectionProps {
  matchData: {
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
  };
  className?: string;
}

const JobMatchSection: React.FC<JobMatchSectionProps> = ({ matchData, className }) => {
  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="p-5 border-b">
        <h3 className="font-semibold text-lg">Job Match Analysis</h3>
      </div>
      
      <div className="p-5 space-y-6">
        {/* Score cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ScoreCard 
            title="Overall Match" 
            score={matchData.match_score}
            description="How well your resume matches the job requirements"
          />
          <ScoreCard 
            title="Skills Coverage" 
            score={matchData.technical_match.skill_coverage_score}
            description="Percentage of required skills you possess"
          />
          <ScoreCard 
            title="Experience" 
            score={matchData.experience_match.experience_score}
            description={`Required: ${matchData.experience_match.required_years} years, You have: ${matchData.experience_match.actual_years} years`}
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
                {matchData.technical_match.matched_skills.map((skill, index) => (
                  <span key={index} className="chip bg-success/10 text-success border border-success/20">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            
            <div className="space-y-2">
              <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                <X className="h-4 w-4 text-destructive" />
                <span>Missing Skills</span>
              </h5>
              <div className="flex flex-wrap gap-2">
                {matchData.technical_match.missing_skills.map((skill, index) => (
                  <span key={index} className="chip bg-destructive/10 text-destructive border border-destructive/20">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
        
        {/* Requirements section */}
        <div className="space-y-4">
          <h4 className="font-medium">Key Requirements</h4>
          
          <div className="space-y-4">
            {matchData.key_requirements.met.length > 0 && (
              <div className="space-y-2">
                <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <Check className="h-4 w-4 text-success" />
                  <span>Requirements Met</span>
                </h5>
                <ul className="space-y-1">
                  {matchData.key_requirements.met.map((req, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <Check className="h-4 w-4 text-success shrink-0 mt-1" />
                      <span className="text-sm">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {matchData.key_requirements.partially_met.length > 0 && (
              <div className="space-y-2">
                <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <AlertCircle className="h-4 w-4 text-warning" />
                  <span>Partially Met</span>
                </h5>
                <ul className="space-y-1">
                  {matchData.key_requirements.partially_met.map((req, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <AlertCircle className="h-4 w-4 text-warning shrink-0 mt-1" />
                      <span className="text-sm">{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {matchData.key_requirements.not_met.length > 0 && (
              <div className="space-y-2">
                <h5 className="text-sm font-medium text-muted-foreground flex items-center gap-1">
                  <X className="h-4 w-4 text-destructive" />
                  <span>Not Met</span>
                </h5>
                <ul className="space-y-1">
                  {matchData.key_requirements.not_met.map((req, index) => (
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
        {matchData.recommendations.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium">Recommendations</h4>
            <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
              <ul className="space-y-2">
                {matchData.recommendations.map((rec, index) => (
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
