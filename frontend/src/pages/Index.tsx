import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import ResumeHeader from '../components/ResumeHeader';
import SectionAnalysis from '../components/SectionAnalysis';
import JobMatchSection from '../components/JobMatchSection';
import { HealthCheck } from '../components/HealthCheck';
import { FileText, Briefcase, MousePointerClick, Upload, AlertTriangle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { useAnalysisStore } from '@/lib/store';
import { toast } from 'sonner';

const Index = () => {
  const navigate = useNavigate();
  const analysisResult = useAnalysisStore(state => state.analysisResult);
  const [activeTab, setActiveTab] = useState<'sections' | 'jobMatch'>('sections');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Redirect if no analysis result
  useEffect(() => {
    if (!analysisResult) {
      navigate('/');
      return;
    }

    // Verify data structure
    if (!analysisResult.resumeAnalysis?.sections || !Array.isArray(analysisResult.resumeAnalysis.sections)) {
      setError('Invalid analysis result structure');
      toast.error('There was a problem with the analysis result');
    }

    // Remove loading after a short delay for smooth transition
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, [analysisResult, navigate]);

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { type: 'spring', stiffness: 100, damping: 15 }
    }
  };

  if (loading || !analysisResult) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background to-secondary/30">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 rounded-full border-4 border-primary/30 border-t-primary animate-spin"></div>
          <h2 className="text-xl font-medium">Analyzing resume...</h2>
        </div>
      </div>
    );
  }

  const sections = analysisResult.resumeAnalysis.sections;
  const matchScore = analysisResult.jobMatchAnalysis?.match_score ?? 0;

  // Function to sort sections in the desired order
  const sortSections = (sections: any[]) => {
    const order = ['Experience', 'Education', 'Projects'];
    return [...sections].sort((a, b) => {
      const indexA = order.indexOf(a.type);
      const indexB = order.indexOf(b.type);
      // If section type is not in our order array, put it at the end
      if (indexA === -1) return 1;
      if (indexB === -1) return -1;
      return indexA - indexB;
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/30">
      <ResumeHeader matchScore={matchScore} />
      
      {/* Add HealthCheck component */}
      <div className="max-w-screen-xl mx-auto px-4 mb-4">
        <HealthCheck />
      </div>
      
      {/* Navigation tabs */}
      <div className="max-w-screen-xl mx-auto px-4 mb-4 sm:mb-8">
        <div className="flex flex-wrap gap-1 sm:gap-4 border-b pb-2">
          <button
            onClick={() => setActiveTab('sections')}
            className={`flex items-center gap-1 sm:gap-2 px-3 sm:px-4 py-2 rounded-t-lg font-medium text-sm sm:text-base transition-all ${
              activeTab === 'sections' 
                ? 'bg-primary text-primary-foreground' 
                : 'hover:bg-secondary'
            }`}
          >
            <FileText className="h-4 w-4" />
            <span>Resume Sections</span>
          </button>
          {analysisResult.jobMatchAnalysis && (
            <button
              onClick={() => setActiveTab('jobMatch')}
              className={`flex items-center gap-1 sm:gap-2 px-3 sm:px-4 py-2 rounded-t-lg font-medium text-sm sm:text-base transition-all ${
                activeTab === 'jobMatch' 
                  ? 'bg-primary text-primary-foreground' 
                  : 'hover:bg-secondary'
              }`}
            >
              <Briefcase className="h-4 w-4" />
              <span>Job Match</span>
            </button>
          )}
        </div>
      </div>
      
      <motion.div 
        className="max-w-screen-xl mx-auto px-4 pb-16 sm:pb-20"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {activeTab === 'sections' && (
          <motion.div className="space-y-6 sm:space-y-8" variants={itemVariants}>
            {sections.length > 0 ? (
              sortSections(sections).map((section, index) => {
                // Temporarily hide Skills section
                if (section.type === 'Skills') {
                  return null;
                }
                return (
                  <SectionAnalysis
                    key={index}
                    title={section.type}
                    section={section}
                  />
                );
              })
            ) : (
              <div className="flex flex-col items-center justify-center py-8 sm:py-12 text-center">
                <AlertTriangle className="h-10 w-10 sm:h-12 sm:w-12 text-warning mb-3 sm:mb-4" />
                <h3 className="text-lg sm:text-xl font-medium mb-2">No resume sections found</h3>
                <p className="text-sm sm:text-base text-muted-foreground">It seems like there are no sections in the analysis result.</p>
              </div>
            )}
          </motion.div>
        )}
        
        {activeTab === 'jobMatch' && analysisResult.jobMatchAnalysis && (
          <motion.div variants={itemVariants}>
            <JobMatchSection matchData={analysisResult.jobMatchAnalysis} />
          </motion.div>
        )}

        <motion.div 
          variants={itemVariants}
          className="mt-8 sm:mt-10 text-center"
        >
          <Button asChild className="px-6 sm:px-8 py-4 sm:py-6 text-base sm:text-lg">
            <Link to="/" className="inline-flex items-center gap-2">
              <Upload className="w-4 h-4 sm:w-5 sm:h-5" />
              Analyze Another Resume
            </Link>
          </Button>
        </motion.div>
      </motion.div>
      
      {/* Quick navigation fixed button */}
      <div className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6">
        <div className="relative group">
          <button 
            className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center shadow-elevation-medium hover:shadow-elevation-high transition-all"
            aria-label="Quick navigation"
          >
            <MousePointerClick className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
          
          <div className="absolute bottom-full right-0 mb-2 hidden group-hover:block animate-fade-in">
            <div className="bg-card rounded-lg shadow-elevation-medium p-2 border flex flex-col gap-2 w-40 sm:w-48">
              <button
                onClick={() => setActiveTab('sections')}
                className={`flex items-center gap-2 p-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'sections' ? 'bg-primary/10 text-primary' : 'hover:bg-secondary'
                }`}
              >
                <FileText className="h-4 w-4" />
                <span>Resume Sections</span>
              </button>
              {analysisResult.jobMatchAnalysis && (
                <button
                  onClick={() => setActiveTab('jobMatch')}
                  className={`flex items-center gap-2 p-2 rounded-md text-sm font-medium transition-all ${
                    activeTab === 'jobMatch' ? 'bg-primary/10 text-primary' : 'hover:bg-secondary'
                  }`}
                >
                  <Briefcase className="h-4 w-4" />
                  <span>Job Match</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
