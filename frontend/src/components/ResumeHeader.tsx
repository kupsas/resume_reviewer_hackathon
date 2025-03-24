import React from 'react';
import { FileText } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ResumeHeaderProps {
  matchScore: number;
  className?: string;
}

const ResumeHeader: React.FC<ResumeHeaderProps> = ({ matchScore, className }) => {
  return (
    <div className={cn(
      "w-full max-w-screen-xl mx-auto px-4 py-6 md:py-10", 
      "bg-gradient-to-r from-primary/5 via-background to-accent/5", 
      className
    )}>
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
          <FileText className="w-6 h-6 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl md:text-3xl font-semibold text-foreground">Resume Analysis</h1>
          <p className="text-muted-foreground">
            {matchScore === 0 
              ? "Your resume has been analyzed. Add a job description to see match analysis!"
              : "Your resume has been analyzed for job compatibility"}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResumeHeader;
