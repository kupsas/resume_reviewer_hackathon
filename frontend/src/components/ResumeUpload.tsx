'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface ResumeUploadProps {
  onFileSelect: (file: File) => void;
}

export default function ResumeUpload({ onFileSelect }: ResumeUploadProps) {
  const [fileName, setFileName] = useState<string>('');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setFileName(file.name);
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false
  });

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
      >
        <input {...getInputProps()} />
        <div className="space-y-4">
          <div className="flex justify-center">
            <svg
              className={`w-12 h-12 ${isDragActive ? 'text-blue-500' : 'text-gray-400'}`}
              fill="none"
              strokeWidth="1.5"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"
              />
            </svg>
          </div>
          
          <div className="text-lg">
            {fileName ? (
              <p className="text-blue-600">Selected: {fileName}</p>
            ) : (
              <>
                <p className="font-semibold">
                  Drop your resume here or click to browse
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Supports PDF and DOCX files
                </p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 