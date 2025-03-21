
import React from 'react';
import { cn } from '@/lib/utils';

interface ScoreCardProps {
  title: string;
  score: number;
  maxScore?: number;
  className?: string;
  description?: string;
}

const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  maxScore = 100,
  className,
  description
}) => {
  const percentage = (score / maxScore) * 100;
  
  const getScoreColor = (percentage: number) => {
    if (percentage >= 80) return "bg-success";
    if (percentage >= 60) return "bg-warning";
    return "bg-destructive";
  };

  const getBgColor = (percentage: number) => {
    if (percentage >= 80) return "bg-success/5 hover:bg-success/10";
    if (percentage >= 60) return "bg-warning/5 hover:bg-warning/10";
    return "bg-destructive/5 hover:bg-destructive/10";
  };

  return (
    <div className={cn(
      "rounded-xl p-4 border transition-all duration-300",
      "hover:shadow-elevation-low",
      getBgColor(percentage),
      className
    )}>
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-medium text-sm text-muted-foreground">{title}</h3>
        <div className="font-semibold text-lg">
          {score}
          {maxScore !== 100 && <span className="text-muted-foreground text-sm">/{maxScore}</span>}
        </div>
      </div>
      
      {description && (
        <p className="text-sm text-muted-foreground mb-2">{description}</p>
      )}
      
      <div className="progress-bar mt-1 bg-secondary">
        <div 
          className={cn("progress-bar-value", getScoreColor(percentage))}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ScoreCard;
