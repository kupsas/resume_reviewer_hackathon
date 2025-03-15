'use client';

import { useState } from 'react';
import AnalysisResults from '@/components/AnalysisResults';
import FullScreenLoader from '@/components/FullScreenLoader';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setError(null);
    }
  };

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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500">
          AI Resume Reviewer
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6 mb-8">
          <div>
            <label className="block text-sm font-medium mb-2">Upload Resume (PDF or DOCX)</label>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              className="w-full p-2 rounded bg-gray-800 border border-gray-700"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Job Description (Optional)</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full p-2 rounded bg-gray-800 border border-gray-700 h-32"
              placeholder="Paste the job description here for targeted analysis..."
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 px-4 rounded bg-blue-600 hover:bg-blue-700 transition-colors"
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </form>

        {error && (
          <div className="text-red-500 bg-red-900/20 p-4 rounded mb-8">
            {error}
          </div>
        )}

        {loading && <FullScreenLoader />}

        {analysis && <AnalysisResults analysis={analysis} />}
      </div>
    </main>
  );
}
