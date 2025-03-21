
import React, { useState } from 'react';
import StarAnalysisCard from './StarAnalysisCard';
import { cn } from '@/lib/utils';
import { ChevronDown } from 'lucide-react';

interface Point {
  text: string;
  star: {
    situation: boolean;
    task: boolean;
    action: boolean;
    result: boolean;
    complete: boolean;
  };
  metrics: string[];
  technical_score: number;
  improvement: string;
}

interface SectionAnalysisProps {
  title: string;
  points: Point[];
  className?: string;
}

const SectionAnalysis: React.FC<SectionAnalysisProps> = ({
  title,
  points,
  className,
}) => {
  const [expanded, setExpanded] = useState(true);

  const getCompletionPercentage = () => {
    const completePoints = points.filter(point => point.star.complete).length;
    return Math.round((completePoints / points.length) * 100);
  };

  const completionPercentage = getCompletionPercentage();

  return (
    <div className={cn("border rounded-xl overflow-hidden bg-card", className)}>
      <div 
        className="flex items-center justify-between p-4 cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-lg">{title}</h3>
          <div className="flex items-center gap-2">
            <div className="progress-bar w-24">
              <div 
                className={cn(
                  "progress-bar-value",
                  completionPercentage >= 80 ? "bg-success" : 
                  completionPercentage >= 50 ? "bg-warning" : "bg-destructive"
                )}
                style={{ width: `${completionPercentage}%` }}
              />
            </div>
            <span className="text-sm font-medium">{completionPercentage}%</span>
          </div>
        </div>
        
        <ChevronDown className={cn(
          "h-5 w-5 transition-transform duration-200",
          expanded ? "transform rotate-180" : ""
        )} />
      </div>
      
      {expanded && (
        <div className="p-4 pt-0 grid gap-4 grid-cols-1 md:grid-cols-2">
          {points.map((point, index) => (
            <StarAnalysisCard
              key={index}
              text={point.text}
              star={point.star}
              metrics={point.metrics}
              technicalScore={point.technical_score}
              improvement={point.improvement}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default SectionAnalysis;
