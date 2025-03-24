import React from 'react';
import { cn } from '@/lib/utils';
import { EducationPoint } from '@/types/resume';

interface EducationCardProps {
  education: EducationPoint;
  className?: string;
}

// Helper function to get RAG status color
const getRAGColor = (score: number): string => {
  if (score >= 9) return "bg-success/5 border-success/20";
  if (score >= 6) return "bg-warning/5 border-warning/20";
  return "bg-destructive/5 border-destructive/20";
};

const EducationCard: React.FC<EducationCardProps> = ({
  education,
  className
}) => {
  const domesticScore = education.subject_course_school_reputation.domestic_score;
  const internationalScore = education.subject_course_school_reputation.international_score;

  // Helper function to get progress bar color based on score
  const getProgressBarColor = (score: number): string => {
    if (score >= 9) return "bg-success";
    if (score >= 6 && score < 9) return "bg-warning";
    return "bg-muted-foreground/20";
  };

  return (
    <div className={cn(
      "rounded-xl p-5 border bg-card transition-all duration-300 w-full",
      "hover:shadow-elevation-medium",
      className
    )}>
      <div className="flex gap-6 items-stretch w-full min-h-[200px]">
        {/* Main Education Info and Details */}
        <div className="w-1/3 flex flex-col">
          {/* Education Title */}
          <div>
            <h3 className="text-lg font-semibold">{education.course} in {education.subject}</h3>
            <p className="text-base font-medium text-muted-foreground">{education.school}</p>
          </div>
          
          {/* Details Section */}
          <div className="mt-4 border rounded-lg p-4 flex-grow">
            <h4 className="text-sm font-medium mb-2">Details</h4>
            <p className="text-sm text-muted-foreground">
              {education.text}
            </p>
          </div>
        </div>

        {/* Reputation Cards */}
        <div className="flex gap-6 w-2/3 items-end">
          {/* Domestic Reputation Card */}
          <div className={cn(
            "flex-1 p-4 rounded-lg border",
            getRAGColor(domesticScore)
          )}>
            <div className="space-y-3">
              <div className="flex flex-col items-center text-center">
                <span className="text-sm font-bold">
                  Domestic Reputation
                </span>
                <span className={cn(
                  "text-2xl font-bold mt-2",
                  domesticScore >= 9 ? "text-success" : 
                  domesticScore >= 6 ? "text-warning" : 
                  "text-destructive"
                )}>{domesticScore}/10</span>
              </div>
              <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                <div 
                  className={cn(
                    "h-full rounded-full transition-all duration-500",
                    getProgressBarColor(domesticScore)
                  )}
                  style={{ width: `${domesticScore * 10}%` }}
                />
              </div>
              <p className="text-sm text-muted-foreground text-center">
                {education.subject_course_school_reputation.domestic_score_rationale}
              </p>
            </div>
          </div>

          {/* International Reputation Card */}
          <div className={cn(
            "flex-1 p-4 rounded-lg border",
            getRAGColor(internationalScore)
          )}>
            <div className="space-y-3">
              <div className="flex flex-col items-center text-center">
                <span className="text-sm font-bold">
                  International Reputation
                </span>
                <span className={cn(
                  "text-2xl font-bold mt-2",
                  internationalScore >= 9 ? "text-success" : 
                  internationalScore >= 6 ? "text-warning" : 
                  "text-destructive"
                )}>{internationalScore}/10</span>
              </div>
              <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                <div 
                  className={cn(
                    "h-full rounded-full transition-all duration-500",
                    getProgressBarColor(internationalScore)
                  )}
                  style={{ width: `${internationalScore * 10}%` }}
                />
              </div>
              <p className="text-sm text-muted-foreground text-center">
                {education.subject_course_school_reputation.international_score_rationale}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Improvement suggestion if available */}
      {education.improvement && (
        <div className="mt-4">
          <p className="text-sm py-2 px-3 bg-primary/5 rounded-lg border border-primary/10">
            {education.improvement}
          </p>
        </div>
      )}
    </div>
  );
};

export default EducationCard; 