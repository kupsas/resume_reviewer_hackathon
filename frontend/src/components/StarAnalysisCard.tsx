import React from 'react';
import { cn } from '@/lib/utils';
import { Check, X } from 'lucide-react';

interface StarAnalysis {
  situation: boolean;
  task: boolean;
  action: boolean;
  result: boolean;
  complete: boolean;
}

interface StarAnalysisCardProps {
  text: string;
  star?: StarAnalysis;
  metrics: string[];
  improvement: string;
  technicalScore?: number;
  className?: string;
}

const StarAnalysisCard: React.FC<StarAnalysisCardProps> = ({
  text,
  star,
  metrics,
  improvement,
  technicalScore,
  className
}) => {
  return (
    <div className={cn(
      "rounded-xl p-5 border bg-card transition-all duration-300",
      "hover:shadow-elevation-medium",
      className
    )}>
      <div className="space-y-4">
        {/* Original text */}
        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-1">Original</h4>
          <p className="text-base">{text}</p>
        </div>

        {/* STAR Analysis - Only show if star data exists */}
        {star && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-2">STAR Analysis</h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <div className="flex items-center gap-1">
                <span className={cn(
                  "w-5 h-5 rounded-full flex items-center justify-center",
                  star.situation 
                    ? "bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400" 
                    : "bg-destructive/20 text-destructive"
                )}>
                  {star.situation ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                </span>
                <span className="text-sm">Situation</span>
              </div>
              <div className="flex items-center gap-1">
                <span className={cn(
                  "w-5 h-5 rounded-full flex items-center justify-center",
                  star.task 
                    ? "bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400" 
                    : "bg-destructive/20 text-destructive"
                )}>
                  {star.task ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                </span>
                <span className="text-sm">Task</span>
              </div>
              <div className="flex items-center gap-1">
                <span className={cn(
                  "w-5 h-5 rounded-full flex items-center justify-center",
                  star.action 
                    ? "bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400" 
                    : "bg-destructive/20 text-destructive"
                )}>
                  {star.action ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                </span>
                <span className="text-sm">Action</span>
              </div>
              <div className="flex items-center gap-1">
                <span className={cn(
                  "w-5 h-5 rounded-full flex items-center justify-center",
                  star.result 
                    ? "bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400" 
                    : "bg-destructive/20 text-destructive"
                )}>
                  {star.result ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                </span>
                <span className="text-sm">Result</span>
              </div>
            </div>
          </div>
        )}

        {/* Technical Score - Only show if provided */}
        {technicalScore !== undefined && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-2">Technical Score</h4>
            <div className="flex items-center">
              <div className="bg-secondary h-2 w-full rounded-full">
                <div 
                  className="bg-primary h-2 rounded-full" 
                  style={{ width: `${(technicalScore / 5) * 100}%` }}
                />
              </div>
              <span className="ml-2 text-sm font-medium">{technicalScore}/5</span>
            </div>
          </div>
        )}

        {/* Metrics */}
        {metrics.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-2">Metrics</h4>
            <div className="flex flex-wrap gap-2">
              {metrics.map((metric, index) => (
                <span key={index} className="chip bg-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs">
                  {metric}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Improvement - Only show if provided */}
        {improvement && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-1">Suggested Improvement</h4>
            <p className="text-sm py-2 px-3 bg-primary/5 rounded-lg border border-primary/10">{improvement}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StarAnalysisCard;
