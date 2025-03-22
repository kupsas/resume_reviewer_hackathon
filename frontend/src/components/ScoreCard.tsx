import React from 'react';
import { cn } from '@/lib/utils';

interface ScoreCardProps {
  title: string;
  score: number;
  description: string;
  className?: string;
}

const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  description,
  className,
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600";
    if (score > 75) return "text-amber-500";
    return "text-red-500";
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
      "rounded-xl p-5 border bg-card",
      getScoreBackground(score),
      getScoreBorder(score),
      className
    )}>
      <div className="space-y-2">
        <h4 className="font-medium">{title}</h4>
        <div className={cn("text-3xl font-bold", getScoreColor(score))}>
          {score}%
        </div>
        <p className="text-sm text-muted-foreground">
          {description}
        </p>
      </div>
    </div>
  );
};

export default ScoreCard;
