import React from 'react';
import { cn } from '@/lib/utils';
import { ArrowRight, LightbulbIcon, PencilIcon, BookOpenIcon } from 'lucide-react';
import { mockResumeData } from '@/mocks';

// Original interface for reference, keeping for future expansion
/*
interface ImprovementItem {
  original_point: string;
  improved_version: string;
}

interface ImprovementData {
  experience_projects: ImprovementItem[];
  education: string;
  skills_certs: string;
}
*/

interface ImprovementItem {
  original_point: string;
  improved_version: string;
}

interface ImprovementSuggestionsProps {
  recommendations: string[];
  className?: string;
}

const ImprovementSuggestions: React.FC<ImprovementSuggestionsProps> = ({
  recommendations,
  className
}) => {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className={cn("rounded-xl border bg-card", className)}>
        <div className="p-5 border-b">
          <h3 className="font-semibold text-lg">Improvement Suggestions</h3>
        </div>
        <div className="p-5 text-center text-muted-foreground">
          <p>No improvement suggestions available.</p>
        </div>
      </div>
    );
  }

  // Extract example improvements from mock data
  const experienceImprovements: ImprovementItem[] = mockResumeData.resumeAnalysis.sections
    .find(section => section.type === 'Experience')?.points
    .filter(point => point.improvement)
    .map(point => ({
      original_point: point.text,
      improved_version: point.improvement
    })) || [];

  // Categorize recommendations into groups (just for UI organization)
  const experienceRecommendations = recommendations.filter(rec => 
    rec.toLowerCase().includes('experience') || 
    rec.toLowerCase().includes('bullet point') ||
    rec.toLowerCase().includes('star format')
  );
  
  const educationRecommendations = recommendations.filter(rec => 
    rec.toLowerCase().includes('education') || 
    rec.toLowerCase().includes('course') ||
    rec.toLowerCase().includes('degree')
  );
  
  const skillsRecommendations = recommendations.filter(rec => 
    rec.toLowerCase().includes('skill') || 
    rec.toLowerCase().includes('technical') ||
    rec.toLowerCase().includes('proficiency')
  );
  
  // Other recommendations that don't fit into the above categories
  const otherRecommendations = recommendations.filter(rec => 
    !experienceRecommendations.includes(rec) && 
    !educationRecommendations.includes(rec) && 
    !skillsRecommendations.includes(rec)
  );

  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="p-5 border-b">
        <h3 className="font-semibold text-lg">Improvement Suggestions</h3>
      </div>
      
      <div className="p-5 space-y-6">
        {/* Experience improvements with examples */}
        <div className="space-y-4">
          <h4 className="font-medium flex items-center gap-2">
            <PencilIcon className="h-4 w-4 text-primary" />
            Experience & Projects
          </h4>
          
          {/* Example improvements showing before/after */}
          <div className="space-y-4">
            {experienceImprovements.slice(0, 2).map((item, index) => (
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

          {/* Recommendations for experience */}
          {experienceRecommendations.length > 0 && (
            <div className="space-y-2 mt-4">
              <h5 className="text-sm font-medium text-muted-foreground">Recommendations</h5>
              {experienceRecommendations.map((recommendation, index) => (
                <div key={index} className="bg-primary/5 border border-primary/10 rounded-lg p-3">
                  <p className="text-sm">{recommendation}</p>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* Education suggestions */}
        {educationRecommendations.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium flex items-center gap-2">
              <BookOpenIcon className="h-4 w-4 text-primary" />
              Education
            </h4>
            <div className="space-y-2">
              {educationRecommendations.map((recommendation, index) => (
                <div key={index} className="bg-primary/5 border border-primary/10 rounded-lg p-3">
                  <p className="text-sm">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Skills suggestions */}
        {skillsRecommendations.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium flex items-center gap-2">
              <LightbulbIcon className="h-4 w-4 text-primary" />
              Skills & Certifications
            </h4>
            <div className="space-y-2">
              {skillsRecommendations.map((recommendation, index) => (
                <div key={index} className="bg-primary/5 border border-primary/10 rounded-lg p-3">
                  <p className="text-sm">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Other suggestions */}
        {otherRecommendations.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium flex items-center gap-2">
              <ArrowRight className="h-4 w-4 text-primary" />
              General Improvements
            </h4>
            <div className="space-y-2">
              {otherRecommendations.map((recommendation, index) => (
                <div key={index} className="bg-primary/5 border border-primary/10 rounded-lg p-3">
                  <p className="text-sm">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImprovementSuggestions;
