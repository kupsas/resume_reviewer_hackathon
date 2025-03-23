import React from 'react';
import { cn } from '@/lib/utils';
import { ArrowDown, ArrowRight, AlertTriangle } from 'lucide-react';

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
  // Handle potentially missing data
  const experience_projects = improvements?.experience_projects || [];
  const education = improvements?.education || '';
  const skills_certs = improvements?.skills_certs || '';

  // Check if we have any improvements to show
  const hasImprovements = 
    experience_projects.length > 0 ||
    education.trim().length > 0 ||
    skills_certs.trim().length > 0;

  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="p-5 border-b">
        <h3 className="font-semibold text-lg">Section Improvement Suggestions</h3>
      </div>
      
      <div className="p-5 space-y-6">
        {!hasImprovements && (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <AlertTriangle className="h-10 w-10 text-warning mb-4" />
            <h4 className="text-lg font-medium mb-2">No improvements available</h4>
            <p className="text-muted-foreground max-w-md">
              We couldn't find any specific improvements for your resume sections. Try providing a job description for more tailored suggestions.
            </p>
          </div>
        )}
        
        {/* Experience/Projects improvements */}
        {experience_projects.length > 0 && (
          <div className="space-y-4">
            <h4 className="font-medium">Experience & Projects</h4>
            
            <div className="space-y-4">
              {experience_projects.map((item, index) => (
                <div key={index} className="rounded-lg border p-4">
                  <div className="grid grid-cols-1 md:grid-cols-[1fr,auto,1fr] gap-4 items-center">
                    <div>
                      <h5 className="text-sm font-medium text-muted-foreground mb-1">Original</h5>
                      <p className="text-sm">{item.original_point}</p>
                    </div>
                    
                    <div className="flex items-center justify-center">
                      <ArrowRight className="h-5 w-5 text-primary hidden md:block" />
                      <ArrowDown className="h-5 w-5 text-primary md:hidden" />
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
        {education && (
          <div className="space-y-3">
            <h4 className="font-medium">Education</h4>
            <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
              <p className="text-sm">{education}</p>
            </div>
          </div>
        )}
        
        {/* Skills & Certifications suggestion */}
        {skills_certs && (
          <div className="space-y-3">
            <h4 className="font-medium">Skills & Certifications</h4>
            <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
              <p className="text-sm">{skills_certs}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImprovementSuggestions;
