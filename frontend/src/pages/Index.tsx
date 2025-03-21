import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import ResumeHeader from '@/components/ResumeHeader';
import SectionAnalysis from '@/components/SectionAnalysis';
import JobMatchSection from '@/components/JobMatchSection';
import ImprovementSuggestions from '@/components/ImprovementSuggestions';
import { mockResumeData } from '@/mocks';
import { FileText, Briefcase, LineChart, MousePointerClick, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Index = () => {
  const [activeTab, setActiveTab] = useState<'sections' | 'jobMatch' | 'improvements'>('sections');
  const [loading, setLoading] = useState(true);
  const resumeData = mockResumeData;

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
      <div className="max-w-screen-xl mx-auto px-4 pt-8 pb-20">
        <motion.div
          className="grid grid-cols-1 gap-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Header */}
          <motion.div variants={itemVariants}>
            <ResumeHeader 
              overallScore={resumeData.resumeAnalysis.scores.overall * 100} 
              jobMatchScore={resumeData.jobMatchAnalysis?.match_score ? resumeData.jobMatchAnalysis.match_score * 100 : undefined}
            />
          </motion.div>

          {/* Demo Access Button */}
          <motion.div variants={itemVariants} className="flex justify-center mb-4">
            <Link to="/upload">
              <Button className="bg-primary hover:bg-primary/90 text-white">
                <Upload className="mr-2 h-4 w-4" />
                Upload Your Resume
              </Button>
            </Link>
          </motion.div>

          {/* Tabs */}
          <motion.div variants={itemVariants} className="flex flex-wrap justify-center gap-2 mb-6">
            <Button
              variant={activeTab === 'sections' ? 'default' : 'outline'}
              className="flex items-center gap-2"
              onClick={() => setActiveTab('sections')}
            >
              <FileText className="h-4 w-4" />
              <span className="hidden sm:inline">Resume Sections</span>
              <span className="sm:hidden">Sections</span>
            </Button>
            
            {resumeData.jobMatchAnalysis && (
              <Button
                variant={activeTab === 'jobMatch' ? 'default' : 'outline'}
                className="flex items-center gap-2"
                onClick={() => setActiveTab('jobMatch')}
              >
                <Briefcase className="h-4 w-4" />
                <span className="hidden sm:inline">Job Match</span>
                <span className="sm:hidden">Job</span>
              </Button>
            )}
            
            <Button
              variant={activeTab === 'improvements' ? 'default' : 'outline'}
              className="flex items-center gap-2"
              onClick={() => setActiveTab('improvements')}
            >
              <LineChart className="h-4 w-4" />
              <span className="hidden sm:inline">Improvement Suggestions</span>
              <span className="sm:hidden">Improve</span>
            </Button>
          </motion.div>

          {/* Tab Content */}
          <motion.div variants={itemVariants}>
            {activeTab === 'sections' && (
              <div className="space-y-6">
                {resumeData.resumeAnalysis.sections.map((section, index) => (
                  <SectionAnalysis key={index} section={section} />
                ))}
              </div>
            )}
            
            {activeTab === 'jobMatch' && resumeData.jobMatchAnalysis && (
              <JobMatchSection jobMatchAnalysis={resumeData.jobMatchAnalysis} />
            )}
            
            {activeTab === 'improvements' && (
              <ImprovementSuggestions recommendations={resumeData.resumeAnalysis.recommendations} />
            )}
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Index;
