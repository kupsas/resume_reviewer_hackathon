
import React from 'react';
import { cn } from '@/lib/utils';
import { ArrowRight } from 'lucide-react';

interface ImprovementItem {
  original_point: string;
  improved_version: string;
}

interface ImprovementSuggestionsProps {
  improvements: {
    experience_projects: ImprovementItem[];
    education: string;
    skills_certs: string;
  };
  className?: string;
}

const ImprovementSuggestions: React.FC<ImprovementSuggestionsProps> = ({
  improvements,
  className
}) => {
  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="p-5 border-b">
        <h3 className="font-semibold text-lg">Section Improvement Suggestions</h3>
      </div>
      
      <div className="p-5 space-y-6">
        {/* Experience/Projects improvements */}
        {improvements.experience_projects.length > 0 && (
          <div className="space-y-4">
            <h4 className="font-medium">Experience & Projects</h4>
            
            <div className="space-y-4">
              {improvements.experience_projects.map((item, index) => (
                <div key={index} className="rounded-lg border p-4">
                  <div className="flex flex-col gap-3">
                    <div>
                      <h5 className="text-sm font-medium text-muted-foreground mb-1">Original</h5>
                      <p className="text-sm">{item.original_point}</p>
                    </div>
                    
                    <div className="flex items-center justify-center">
                      <ArrowRight className="h-5 w-5 text-primary" />
                    </div>
                    
                    <div>
                      <h5 className="text-sm font-medium text-muted-foreground mb-1">Improved</h5>
                      <p className="text-sm py-2 px-3 bg-primary/5 rounded-lg border border-primary/10">
                        {item.improved_version}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Education suggestion */}
        {improvements.education && (
          <div className="space-y-3">
            <h4 className="font-medium">Education</h4>
            <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
              <p className="text-sm">{improvements.education}</p>
            </div>
          </div>
        )}
        
        {/* Skills & Certifications suggestion */}
        {improvements.skills_certs && (
          <div className="space-y-3">
            <h4 className="font-medium">Skills & Certifications</h4>
            <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
              <p className="text-sm">{improvements.skills_certs}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImprovementSuggestions;
