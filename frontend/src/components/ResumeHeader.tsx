import React from 'react';
import { FileText, Check, AlertTriangle, Info } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ResumeHeaderProps {
  matchScore: number;
  className?: string;
}

const ResumeHeader: React.FC<ResumeHeaderProps> = ({ matchScore, className }) => {
  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600";
    if (score > 75) return "text-amber-500";
    return "text-red-500";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return "Excellent Match";
    if (score > 75) return "Good Match";
    return "Needs Improvement";
  };

  const getScoreIcon = (score: number) => {
    if (score >= 90) return <Check className="h-5 w-5 text-green-600" />;
    if (score > 75) return <Info className="h-5 w-5 text-amber-500" />;
    return <AlertTriangle className="h-5 w-5 text-red-500" />;
  };

  const getScoreBackground = (score: number) => {
    if (score >= 90) return "bg-green-100";
    if (score > 75) return "bg-amber-100";
    return "bg-red-100";
  };

  const getScoreBorder = (score: number) => {
    if (score >= 90) return "border-green-300";
    if (score > 75) return "border-amber-300";
    return "border-red-300";
  };

  return (
    <div className={cn(
      "w-full max-w-screen-xl mx-auto px-4 py-6 md:py-10", 
      "bg-gradient-to-r from-primary/5 via-background to-accent/5", 
      className
    )}>
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 md:gap-8">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <FileText className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-semibold">Resume Analysis</h1>
            <p className="text-muted-foreground">
              {matchScore === 0 
                ? "Your resume has been analyzed. Add a job description to see match analysis!"
                : "Your resume has been analyzed for job compatibility"}
            </p>
          </div>
        </div>
        
        {matchScore !== null && matchScore > 0 ? (
          <div className={cn(
            "flex items-center gap-2 p-3 rounded-xl",
            getScoreBackground(matchScore),
            getScoreBorder(matchScore),
            "border transition-all duration-300"
          )}>
            <div className="flex flex-col items-center">
              <div className="text-3xl font-bold">{matchScore}%</div>
              <div className={cn("text-sm font-medium flex items-center gap-1", getScoreColor(matchScore))}>
                {getScoreIcon(matchScore)}
                <span>{getScoreLabel(matchScore)}</span>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default ResumeHeader;
