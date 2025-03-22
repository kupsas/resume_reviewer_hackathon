import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import ResumeHeader from '@/components/ResumeHeader';
import SectionAnalysis from '@/components/SectionAnalysis';
import JobMatchSection from '@/components/JobMatchSection';
import ImprovementSuggestions from '@/components/ImprovementSuggestions';
import { sampleResumeData } from '@/data/sampleResumeData';
import { FileText, Briefcase, LineChart, MousePointerClick, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Index = () => {
  const [activeTab, setActiveTab] = useState<'sections' | 'jobMatch' | 'improvements'>('sections');
  const [loading, setLoading] = useState(true);

  // Simulate loading from API
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background to-secondary/30">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 rounded-full border-4 border-primary/30 border-t-primary animate-spin"></div>
          <h2 className="text-xl font-medium">Analyzing resume...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/30">
      <ResumeHeader matchScore={sampleResumeData.jobMatchAnalysis.match_score} />
      
      {/* Navigation tabs */}
      <div className="max-w-screen-xl mx-auto px-4 mb-8">
        <div className="flex flex-wrap gap-2 sm:gap-4 border-b pb-2">
          <button
            onClick={() => setActiveTab('sections')}
            className={`flex items-center gap-2 px-4 py-2 rounded-t-lg font-medium transition-all ${
              activeTab === 'sections' 
                ? 'bg-primary text-primary-foreground' 
                : 'hover:bg-secondary'
            }`}
          >
            <FileText className="h-4 w-4" />
            <span>Resume Sections</span>
          </button>
          <button
            onClick={() => setActiveTab('jobMatch')}
            className={`flex items-center gap-2 px-4 py-2 rounded-t-lg font-medium transition-all ${
              activeTab === 'jobMatch' 
                ? 'bg-primary text-primary-foreground' 
                : 'hover:bg-secondary'
            }`}
          >
            <Briefcase className="h-4 w-4" />
            <span>Job Match</span>
          </button>
          <button
            onClick={() => setActiveTab('improvements')}
            className={`flex items-center gap-2 px-4 py-2 rounded-t-lg font-medium transition-all ${
              activeTab === 'improvements' 
                ? 'bg-primary text-primary-foreground' 
                : 'hover:bg-secondary'
            }`}
          >
            <LineChart className="h-4 w-4" />
            <span>Improvements</span>
          </button>
        </div>
      </div>
      
      <motion.div 
        className="max-w-screen-xl mx-auto px-4 pb-16"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {activeTab === 'sections' && (
          <motion.div className="space-y-8" variants={itemVariants}>
            {sampleResumeData.resumeAnalysis.sections.map((section, index) => (
              <SectionAnalysis
                key={index}
                title={section.type}
                points={section.points}
              />
            ))}
          </motion.div>
        )}
        
        {activeTab === 'jobMatch' && (
          <motion.div variants={itemVariants}>
            <JobMatchSection matchData={sampleResumeData.jobMatchAnalysis} />
          </motion.div>
        )}
        
        {activeTab === 'improvements' && (
          <motion.div variants={itemVariants}>
            <ImprovementSuggestions 
              improvements={sampleResumeData.jobMatchAnalysis.section_recommendations}
            />
          </motion.div>
        )}

        <motion.div 
          variants={itemVariants}
          className="mt-10 text-center"
        >
          <Button asChild className="px-8 py-6">
            <Link to="/" className="inline-flex items-center gap-2 text-lg">
              <Upload className="w-5 h-5" />
              Analyze Another Resume
            </Link>
          </Button>
        </motion.div>
      </motion.div>
      
      {/* Quick navigation fixed button */}
      <div className="fixed bottom-6 right-6">
        <div className="relative group">
          <button className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center shadow-elevation-medium hover:shadow-elevation-high transition-all">
            <MousePointerClick className="w-5 h-5" />
          </button>
          
          <div className="absolute bottom-full right-0 mb-2 hidden group-hover:block animate-fade-in">
            <div className="bg-card rounded-lg shadow-elevation-medium p-2 border flex flex-col gap-2 w-48">
              <button
                onClick={() => setActiveTab('sections')}
                className={`flex items-center gap-2 p-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'sections' ? 'bg-primary/10 text-primary' : 'hover:bg-secondary'
                }`}
              >
                <FileText className="h-4 w-4" />
                <span>Resume Sections</span>
              </button>
              <button
                onClick={() => setActiveTab('jobMatch')}
                className={`flex items-center gap-2 p-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'jobMatch' ? 'bg-primary/10 text-primary' : 'hover:bg-secondary'
                }`}
              >
                <Briefcase className="h-4 w-4" />
                <span>Job Match</span>
              </button>
              <button
                onClick={() => setActiveTab('improvements')}
                className={`flex items-center gap-2 p-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'improvements' ? 'bg-primary/10 text-primary' : 'hover:bg-secondary'
                }`}
              >
                <LineChart className="h-4 w-4" />
                <span>Improvements</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
