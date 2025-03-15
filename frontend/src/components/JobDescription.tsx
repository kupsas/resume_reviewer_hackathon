'use client';

import { useState, ChangeEvent } from 'react';

interface JobDescriptionProps {
  onDescriptionChange: (description: string) => void;
}

export default function JobDescription({ onDescriptionChange }: JobDescriptionProps) {
  const [description, setDescription] = useState('');

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    const newDescription = e.target.value;
    setDescription(newDescription);
    onDescriptionChange(newDescription);
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <div className="space-y-4">
        <label 
          htmlFor="jobDescription" 
          className="block text-lg font-semibold text-futuristic-accent"
        >
          Job Description
        </label>
        <p className="text-sm text-gray-400">
          Paste the job description here to get personalized resume feedback
        </p>
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg blur opacity-30 group-hover:opacity-50 transition duration-1000"></div>
          <textarea
            id="jobDescription"
            value={description}
            onChange={handleChange}
            placeholder="Paste job description here..."
            className="relative w-full h-48 p-4 bg-futuristic-dark border border-futuristic-light rounded-lg 
                     text-gray-100 placeholder-gray-500
                     focus:ring-2 focus:ring-futuristic-accent focus:border-transparent 
                     resize-none transition duration-200"
          />
        </div>
      </div>
    </div>
  );
} 