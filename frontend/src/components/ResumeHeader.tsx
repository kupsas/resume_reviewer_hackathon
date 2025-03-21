
import React from 'react';
import { FileText, Check, AlertTriangle, Info } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ResumeHeaderProps {
  matchScore: number;
  className?: string;
}

const ResumeHeader: React.FC<ResumeHeaderProps> = ({ matchScore, className }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-success";
    if (score >= 60) return "text-warning";
    return "text-destructive";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent Match";
    if (score >= 60) return "Good Match";
    return "Needs Improvement";
  };

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <Check className="h-5 w-5 text-success" />;
    if (score >= 60) return <Info className="h-5 w-5 text-warning" />;
    return <AlertTriangle className="h-5 w-5 text-destructive" />;
  };

  const getScoreBackground = (score: number) => {
    if (score >= 80) return "bg-success/10";
    if (score >= 60) return "bg-warning/10";
    return "bg-destructive/10";
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
              Your resume has been analyzed for job compatibility
            </p>
          </div>
        </div>
        
        <div className={cn(
          "flex items-center gap-2 p-3 rounded-xl",
          getScoreBackground(matchScore),
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
      </div>
    </div>
  );
};

export default ResumeHeader;
