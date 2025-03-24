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
    if (score >= 90) return "text-green-600 dark:text-green-400";
    if (score > 75) return "text-amber-500 dark:text-amber-400";
    return "text-red-500 dark:text-red-400";
  };

  const getScoreBackground = (score: number) => {
    if (score >= 90) return "bg-green-100 dark:bg-green-950";
    if (score > 75) return "bg-amber-100 dark:bg-amber-950";
    return "bg-red-100 dark:bg-red-950";
  };

  const getScoreBorder = (score: number) => {
    if (score >= 90) return "border-green-300 dark:border-green-800";
    if (score > 75) return "border-amber-300 dark:border-amber-800";
    return "border-red-300 dark:border-red-800";
  };

  return (
    <div className={cn(
      "rounded-xl p-5 border bg-card",
      getScoreBackground(score),
      getScoreBorder(score),
      className
    )}>
      <div className="space-y-2">
        <h4 className="font-medium text-foreground">{title}</h4>
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
