import React, { useState } from 'react';
import StarAnalysisCard from './StarAnalysisCard';
import JobMatchSection from './JobMatchSection';
import { Button } from './ui/button';
import { Loader2, Upload, FileText } from 'lucide-react';
import { useResumeAnalysis } from '@/hooks/useResumeAnalysis';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

const ResumeAnalysis: React.FC = () => {
  const { loading, error, analysisResult, analyzeResume, analyzeResumeText } = useResumeAnalysis();
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleFileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resumeFile) return;
    await analyzeResume(resumeFile, jobDescription);
  };

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resumeText.trim()) return;
    await analyzeResumeText(resumeText, jobDescription);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <Tabs defaultValue="file" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="file" className="flex items-center gap-2">
            <Upload className="w-4 h-4" />
            Upload File
          </TabsTrigger>
          <TabsTrigger value="text" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Paste Text
          </TabsTrigger>
        </TabsList>

        <TabsContent value="file">
          <form onSubmit={handleFileSubmit} className="space-y-4">
            <div>
              <label htmlFor="resume-upload" className="block text-sm font-medium mb-2">
                Upload Resume (PDF)
              </label>
              <Input
                id="resume-upload"
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                aria-label="Upload Resume PDF"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Job Description (Optional)</label>
              <Textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="min-h-[100px]"
              />
            </div>

            <Button type="submit" disabled={loading || !resumeFile}>
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
        </TabsContent>

        <TabsContent value="text">
          <form onSubmit={handleTextSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Resume Text</label>
              <Textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste your resume text here..."
                className="min-h-[200px]"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Job Description (Optional)</label>
              <Textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="min-h-[100px]"
              />
            </div>

            <Button type="submit" disabled={loading || !resumeText.trim()}>
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
        </TabsContent>
      </Tabs>

      {/* Error Message */}
      {error && (
        <div className="bg-destructive/10 text-destructive p-4 rounded-lg">
          {error instanceof Error ? error.message : 'An error occurred while analyzing your resume.'}
        </div>
      )}

      {/* Analysis Results */}
      {analysisResult && (
        <div className="space-y-8">
          {/* Job Match Section */}
          {analysisResult.jobMatchAnalysis && (
            <JobMatchSection matchData={analysisResult.jobMatchAnalysis} />
          )}

          {/* Resume Sections */}
          <div className="space-y-8">
            <h3 className="font-semibold text-lg">Resume Analysis</h3>
            {analysisResult.resumeAnalysis.sections.map((section, sectionIndex) => (
              <div key={sectionIndex} className="space-y-4">
                <h4 className="font-medium text-md text-muted-foreground">{section.type}</h4>
                {section.points.map((point, pointIndex) => (
                  <StarAnalysisCard
                    key={`${sectionIndex}-${pointIndex}`}
                    text={point.text}
                    star={point.star}
                    metrics={point.metrics}
                    technicalScore={point.technical_score}
                    improvement={point.improvement}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalysis;
