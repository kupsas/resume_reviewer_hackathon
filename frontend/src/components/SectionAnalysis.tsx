import React, { useState } from 'react';
import { cn, isEducationPoint } from '@/lib/utils';
import { ResumePoint, ResumeSection, StandardResumePoint } from '@/types/resume';
import { ChevronDown } from 'lucide-react';
import StarAnalysisCard from './StarAnalysisCard';
import EducationCard from './EducationCard';

interface SectionAnalysisProps {
  title: string;
  section: ResumeSection;
  className?: string;
}

const SectionAnalysis: React.FC<SectionAnalysisProps> = ({
  title,
  section,
  className,
}) => {
  const [expanded, setExpanded] = useState(true);
  const isEducationSection = section.type === 'Education';

  return (
    <div className={cn("border rounded-xl overflow-hidden bg-card", className)}>
      <div 
        className="flex items-center justify-between p-4 cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-lg">{title}</h3>
        </div>
        
        <ChevronDown className={cn(
          "h-5 w-5 transition-transform duration-200",
          expanded ? "transform rotate-180" : ""
        )} />
      </div>
      
      {expanded && (
        <div className={cn(
          "p-4 pt-0 grid gap-4",
          isEducationSection ? "grid-cols-1" : "grid-cols-1 md:grid-cols-2"
        )}>
          {section.points.map((point, index) => {
            // Check if this is an education point
            if (isEducationSection && isEducationPoint(point)) {
              return (
                <EducationCard 
                  key={index}
                  education={point}
                />
              );
            } else {
              // Handle as standard resume point
              const standardPoint = point as StandardResumePoint;
              return (
                <StarAnalysisCard
                  key={index}
                  text={standardPoint.text}
                  star={standardPoint.star || {
                    situation: false,
                    task: false,
                    action: false,
                    result: false,
                    complete: false
                  }}
                  metrics={standardPoint.metrics}
                  technicalScore={standardPoint.technical_score}
                  improvement={standardPoint.improvement || ''}
                />
              );
            }
          })}
        </div>
      )}
    </div>
  );
};

export default SectionAnalysis;
