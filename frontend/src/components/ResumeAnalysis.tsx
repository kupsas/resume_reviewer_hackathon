import React, { useState } from 'react';
import { useResumeAnalysis } from '../hooks/useResumeAnalysis';
import StarAnalysisCard from './StarAnalysisCard';
import JobMatchSection from './JobMatchSection';
import { Button } from './ui/button';
import { Loader2 } from 'lucide-react';

const ResumeAnalysis: React.FC = () => {
  const { loading, error, analysisResult, analyzeResume } = useResumeAnalysis();
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription) {
      return;
    }
    await analyzeResume(resumeFile, jobDescription);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      {/* Upload Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Upload Resume (PDF)</label>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="w-full border rounded-lg p-2"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Job Description</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            className="w-full border rounded-lg p-2 min-h-[100px]"
            placeholder="Paste the job description here..."
          />
        </div>

        <Button type="submit" disabled={loading || !resumeFile || !jobDescription}>
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            'Analyze Resume'
          )}
        </Button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="bg-destructive/10 text-destructive p-4 rounded-lg">
          {error}
        </div>
      )}

      {/* Analysis Results */}
      {analysisResult && (
        <div className="space-y-8">
          {/* Job Match Section */}
          <JobMatchSection matchData={analysisResult.jobMatch} />

          {/* Bullet Point Analysis */}
          <div className="space-y-4">
            <h3 className="font-semibold text-lg">Bullet Point Analysis</h3>
            {analysisResult.bulletPoints.map((bullet, index) => (
              <StarAnalysisCard
                key={index}
                text={bullet.text}
                star={bullet.star}
                metrics={bullet.metrics}
                improvement={bullet.improvement}
                technicalScore={bullet.technicalScore}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalysis;
