'use client';

import React from 'react';
import { Analysis, CategoryScore } from './analysis/types';
import { TextFormatter } from './analysis/TextFormatter';
import { AnalysisChart } from './analysis/AnalysisChart';
import { ScoreDisplay } from './analysis/ScoreDisplay';

interface AnalysisResultsProps {
  analysis: Analysis;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysis }) => {
  // Category name mapping for shorter display
  const categoryNameMap: { [key: string]: string } = {
    // Resume strength categories
    'Technical Skills': 'Technical Skills',
    'Experience Quality': 'Experience Quality',
    'Education': 'Education',
    'Resume Format': 'Format',
    'Overall Presentation': 'Presentation',
    // Job match categories
    'Skills Match': 'Skills Match',
    'Experience Match': 'Experience Match',
    'Education Match': 'Education Match',
    'Requirements Match': 'Requirements Match',
    'Overall Fit': 'Overall Fit'
  };

  // Maximum scores for each category
  const maxScores: { [key: string]: number } = {
    // Resume strength categories (20 points each)
    'Technical Skills': 20,
    'Experience Quality': 20,
    'Education': 20,
    'Resume Format': 20,
    'Overall Presentation': 20,
    // Job match categories
    'Skills Match': 25,
    'Experience Match': 25,
    'Education Match': 20,
    'Requirements Match': 20,
    'Overall Fit': 10
  };

  // Split analysis into sections and find relevant ones
  const sections = analysis.analysis
    .split(/(?=(?:\d+\.)?\s*(?:RESUME STRENGTH CATEGORIES|JOB MATCH CATEGORIES))/)
    .filter(Boolean)
    .map(section => section.trim());
  
  // Extract scores for both resume strength and job match
  const strengthSection = sections.find(s => 
    s.includes('RESUME STRENGTH CATEGORIES') || 
    s.includes('1. RESUME STRENGTH CATEGORIES')
  );
  const jobMatchSection = sections.find(s => 
    s.includes('JOB MATCH CATEGORIES') || 
    s.includes('6. JOB MATCH CATEGORIES')
  );
  
  // Helper function to extract scores from a section
  const extractScoresFromSection = (section: string): CategoryScore[] => {
    const lines = section.split('\n');
    const scores: CategoryScore[] = [];
    let foundScores = false;
    let processingSection = '';
    let inScoresSection = false;
    
    for (const line of lines) {
      const trimmedLine = line.trim();
      
      // Identify which section we're processing
      if (trimmedLine.includes('RESUME STRENGTH CATEGORIES')) {
        processingSection = 'resume';
        inScoresSection = true;
        continue;
      } else if (trimmedLine.includes('JOB MATCH CATEGORIES')) {
        processingSection = 'job';
        inScoresSection = true;
        continue;
      } else if (trimmedLine.match(/^\d+\./)) {
        inScoresSection = false;
        if (foundScores) break;
      }
      
      if (!inScoresSection) continue;
      
      // Process score lines
      if (trimmedLine.includes(':')) {
        const [name, scoreStr] = trimmedLine.split(':').map(s => s.trim());
        const score = parseInt(scoreStr);
        
        if (!isNaN(score) && name) {
          foundScores = true;
          const displayName = categoryNameMap[name] || name;
          const maxScore = maxScores[name] || 20;
          const percentage = (score / maxScore) * 100;
          scores.push({
            name,
            displayName,
            score,
            maxScore,
            percentage
          });
        }
      }
    }
    
    return scores;
  };

  // Extract scores for both sections independently
  const strengthScores = strengthSection ? extractScoresFromSection(strengthSection) : [];
  const jobMatchScores = jobMatchSection ? extractScoresFromSection(jobMatchSection) : [];

  // Extract the overall score
  const overallScoreSection = sections.find(s => 
    s.includes('OVERALL RESUME STRENGTH SCORE') || 
    s.includes('OVERALL MATCH SCORE')
  );
  
  const score = overallScoreSection 
    ? parseInt(overallScoreSection.split(':')[1]?.trim() || '0') 
    : null;

  return (
    <div className="bg-gray-800 rounded-lg p-8 shadow-lg border border-gray-700">
      <h1 className="text-3xl font-bold mb-10 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 text-center">
        Resume Analysis Results
      </h1>
      
      <ScoreDisplay score={score} isJobMatch={jobMatchScores.length > 0} />

      {/* Resume Strength Section */}
      {strengthScores.length > 0 && (
        <div className="mb-10">
          <AnalysisChart 
            scores={strengthScores} 
            title="Resume Strength Analysis" 
          />
          <div className="prose prose-invert prose-lg max-w-none mt-10">
            <TextFormatter 
              text={strengthSection || ''} 
              strengthScores={strengthScores}
              jobMatchScores={jobMatchScores}
            />
          </div>
        </div>
      )}

      {/* Job Match Section */}
      {jobMatchScores.length > 0 && (
        <div className="mb-10">
          <AnalysisChart 
            scores={jobMatchScores} 
            title="Job Match Analysis" 
          />
          <div className="prose prose-invert prose-lg max-w-none mt-10">
            <TextFormatter 
              text={jobMatchSection || ''} 
              strengthScores={strengthScores}
              jobMatchScores={jobMatchScores}
            />
          </div>
        </div>
      )}

      {/* Remaining Sections */}
      {sections
        .filter(section => 
          !section.includes('RESUME STRENGTH CATEGORIES') && 
          !section.includes('JOB MATCH CATEGORIES')
        )
        .map((section, index) => (
          <div key={index} className="prose prose-invert prose-lg max-w-none mb-10">
            <TextFormatter 
              text={section} 
              strengthScores={strengthScores}
              jobMatchScores={jobMatchScores}
            />
          </div>
        ))
      }
      
      <div className="mt-10 pt-6 border-t border-gray-700">
        <p className="text-sm text-gray-400 text-center">
          Analysis powered by OpenAI GPT-4
        </p>
      </div>
    </div>
  );
};

export default AnalysisResults; 