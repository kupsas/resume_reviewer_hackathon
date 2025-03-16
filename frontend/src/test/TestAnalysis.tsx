'use client';

import { useState } from 'react';
import AnalysisResults from '../components/AnalysisResults';
import { sampleAnalysisWithJob, sampleAnalysisWithoutJob } from './sample_data';

export default function TestAnalysis() {
  const [showJobMatch, setShowJobMatch] = useState(false);

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">Test Analysis View</h1>
          <button
            onClick={() => setShowJobMatch(!showJobMatch)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            {showJobMatch ? 'Show Without Job Match' : 'Show With Job Match'}
          </button>
        </div>
        
        <AnalysisResults 
          analysis={showJobMatch ? sampleAnalysisWithJob : sampleAnalysisWithoutJob} 
        />
      </div>
    </div>
  );
} 