import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { FileText, Upload as UploadIcon, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import { toast } from 'sonner';
import { useResumeAnalysis } from '@/hooks/useResumeAnalysis';

const Upload = () => {
  const navigate = useNavigate();
  const { analyzeResume, loading: isSubmitting } = useResumeAnalysis();
  const [jobDescription, setJobDescription] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    
    if (file) {
      const fileExtension = file.name.split('.').pop()?.toLowerCase();
      
      if (fileExtension === 'pdf' || fileExtension === 'docx') {
        setSelectedFile(file);
      } else {
        toast.error('Please upload a PDF or DOCX file');
        e.target.value = '';
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFile) {
      toast.error('Please upload your resume');
      return;
    }
    
    try {
      await analyzeResume(selectedFile, jobDescription);
      navigate('/home');
    } catch (error) {
      console.error('Failed to analyze resume:', error);
      // Error toast will be shown by the hook
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/30">
      <div className="max-w-screen-xl mx-auto px-4 pt-10 pb-20">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-8"
        >
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <FileText className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-semibold">Resume Analyzer</h1>
              <p className="text-muted-foreground">
                Upload your resume and get detailed feedback
              </p>
            </div>
          </div>

          <div className="bg-card border rounded-xl p-6 shadow-elevation-low">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="jobDescription" className="text-lg font-medium">
                  Job Description
                </label>
                <Textarea
                  id="jobDescription"
                  placeholder="Paste the job description here (optional)"
                  className="min-h-[200px]"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="text-lg font-medium flex items-center">
                  Resume (PDF or DOCX)
                  <span className="text-destructive ml-1">*</span>
                </label>

                <div className="border-2 border-dashed border-input rounded-lg p-4 transition-colors hover:border-primary/50 focus-within:border-primary">
                  <div className="flex flex-col items-center justify-center gap-2 text-center">
                    <UploadIcon className="w-8 h-8 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">
                      Drag and drop your resume file here or click to browse
                    </p>
                    
                    <div className="mt-2 flex items-center gap-2">
                      <label 
                        htmlFor="file-upload" 
                        className="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium cursor-pointer"
                      >
                        Choose file
                      </label>
                      <span className="text-sm text-muted-foreground">
                        {selectedFile ? selectedFile.name : 'No file chosen'}
                      </span>
                    </div>
                    
                    <input
                      id="file-upload"
                      type="file"
                      className="hidden"
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                    />
                  </div>
                </div>
                
                {!selectedFile && (
                  <div className="flex items-center gap-2 text-destructive text-sm">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Resume is required</span>
                  </div>
                )}
              </div>

              <Button 
                type="submit" 
                className="w-full py-6 text-lg bg-primary"
                disabled={!selectedFile || isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <div className="w-4 h-4 rounded-full border-2 border-current border-t-transparent animate-spin mr-2"></div>
                    Analyzing Resume...
                  </>
                ) : (
                  'Analyze Resume'
                )}
              </Button>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Upload;
