'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import ResumeUpload from '@/components/ResumeUpload';
import AnalysisResults from '@/components/AnalysisResults';
import FullScreenLoader from '@/components/FullScreenLoader';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('resume_file', file);
    if (jobDescription) {
      formData.append('job_description', jobDescription);
    }

    try {
      const response = await fetch('http://localhost:8001/api/resume/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze resume');
      }

      const result = await response.json();
      setAnalysis(result);
      // Scroll to results
      document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
            AI-Powered Resume Review
          </h1>
          <p className="text-gray-400 text-lg">
            Get instant feedback on your resume with our AI-powered analysis tool
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="space-y-4">
            <label className="block text-lg font-medium text-gray-200">
              Upload Your Resume
            </label>
            <ResumeUpload onFileChange={setFile} currentFile={file} />
          </div>

          <div className="space-y-4">
            <label className="block text-lg font-medium text-gray-200">
              Job Description (Optional)
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full p-4 rounded-lg bg-gray-800 border border-gray-700 h-40 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder="Paste the job description here for a more targeted analysis..."
            />
          </div>

          {error && (
            <div className="bg-red-900/20 border border-red-500/50 text-red-400 p-4 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="w-full py-4 px-6 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 font-medium text-lg transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            disabled={loading || !file}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </form>

        {loading && <FullScreenLoader />}

        {analysis && (
          <div id="results" className="mt-16">
            <AnalysisResults analysis={analysis} />
          </div>
        )}
      </main>
    </div>
  );
}
