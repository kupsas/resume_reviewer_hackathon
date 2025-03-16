import React from 'react';
import { CategoryScore } from './types';

interface TextFormatterProps {
  text: string;
  strengthScores: CategoryScore[];
  jobMatchScores: CategoryScore[];
}

export const TextFormatter: React.FC<TextFormatterProps> = ({
  text,
  strengthScores,
  jobMatchScores
}) => {
  // Helper function to check if a line is a category header
  const isCategoryHeader = (line: string) => {
    return line === 'RESUME STRENGTH CATEGORIES' || 
           line === 'JOB MATCH CATEGORIES' ||
           line === 'RESUME STRENGTH CATEGORIES:' || 
           line === 'JOB MATCH CATEGORIES:' ||
           line.includes('1. RESUME STRENGTH CATEGORIES') ||
           line.includes('6. JOB MATCH CATEGORIES');
  };

  // Helper function to check if a line is a score line
  const isScoreLine = (line: string) => {
    return line.includes(':') && (
      strengthScores.some(cat => line.includes(cat.name)) ||
      jobMatchScores.some(cat => line.includes(cat.name))
    );
  };

  // Convert the analysis string to HTML with proper formatting
  const formattedText = text
    .split('\n')
    .map((line, index, lines) => {
      const trimmedLine = line.trim();

      // Skip empty lines
      if (!trimmedLine) return '';

      // Skip category headers and their content
      if (isCategoryHeader(trimmedLine)) {
        return '';
      }

      // Skip individual category score lines
      if (isScoreLine(trimmedLine)) {
        return '';
      }

      // Skip bullet points under categories that are just listing scores
      if ((line.startsWith('• ') || line.startsWith('- ')) && 
        (strengthScores.some(cat => 
          line.toLowerCase().includes(cat.name.toLowerCase()) ||
          line.includes('skills') ||
          line.includes('experience') ||
          line.includes('education') ||
          line.includes('format') ||
          line.includes('presentation')
        ) ||
        jobMatchScores.some(cat =>
          line.toLowerCase().includes(cat.name.toLowerCase())
        ))) {
        return '';
      }

      // Format remaining lines
      if (trimmedLine.startsWith('•') || trimmedLine.startsWith('-')) {
        return `<p class="ml-4 text-gray-300">${trimmedLine}</p>`;
      } else if (/^\d+\./.test(trimmedLine)) {
        return `<h3 class="text-xl font-semibold text-futuristic-accent mt-8 mb-4">${trimmedLine}</h3>`;
      } else {
        return `<p class="text-gray-300">${trimmedLine}</p>`;
      }
    })
    .filter(Boolean) // Remove empty strings
    .join(''); // Join without newlines to prevent extra spacing

  return (
    <div 
      dangerouslySetInnerHTML={{ __html: formattedText }}
      className="space-y-4"
    />
  );
};

const formatLine = (line: string, hasJobMatch: boolean): string => {
  const trimmedLine = line.trim();

  // Skip category headers
  if (trimmedLine === 'RESUME STRENGTH CATEGORIES' || 
      trimmedLine === 'JOB MATCH CATEGORIES' ||
      trimmedLine === 'RESUME STRENGTH CATEGORIES:' || 
      trimmedLine === 'JOB MATCH CATEGORIES:' ||
      trimmedLine.includes('1. RESUME STRENGTH CATEGORIES') ||
      trimmedLine.includes('6. JOB MATCH CATEGORIES')) {
    return '';
  }

  // Skip the overall score lines
  if (line.includes('OVERALL RESUME STRENGTH SCORE') || 
      line.includes('OVERALL MATCH SCORE') ||
      (!hasJobMatch && (
        line.includes('Technical Skills Match') ||
        line.includes('Experience Alignment') ||
        line.includes('Education & Certifications') ||
        line.includes('Soft Skills & Communication') ||
        line.includes('ATS Compatibility')
      ))) {
    return '';
  }

  // Handle section headers and adjust numbering
  if (/^\d+\.\s/.test(line) || (line.toUpperCase() === line.trim() && !line.includes('CATEGORIES'))) {
    const numberedSection = line.match(/^(\d+)\.\s(.+)/);
    if (numberedSection) {
      const [_, num, rest] = numberedSection;
      const sectionNumber = parseInt(num);
      // Adjust section numbers to account for both removed sections
      if (sectionNumber > 1) {
        const newNumber = hasJobMatch ? 
          (sectionNumber > 6 ? sectionNumber - 2 : sectionNumber - 1) : 
          sectionNumber - 1;
        line = `${newNumber}. ${rest}`;
      }
    }
    return `<h2 class="text-2xl font-bold text-futuristic-accent mt-10 mb-6">${line}</h2>`;
  }

  // Handle subsection headers
  if (line.endsWith(':') && !line.includes(':') && line === line.trim()) {
    return `<h3 class="text-xl font-semibold text-futuristic-accent mt-6 mb-3">${line}</h3>`;
  }

  // Handle important categories with colons
  if (line.includes(':') && !line.startsWith('• ') && !line.startsWith('- ') && 
      line.split(':')[0].trim() === line.split(':')[0].trim().toUpperCase()) {
    const [category, content] = line.split(':');
    if (!content || content.trim() === '') {
      return `<h3 class="text-xl font-semibold text-futuristic-accent mt-6 mb-3">${category}:</h3>`;
    } else {
      return `<div class="mb-4">
                <span class="font-semibold text-futuristic-accent">${category}:</span>
                <span class="text-gray-300">${content}</span>
              </div>`;
    }
  }

  // Handle bullet points
  if (line.startsWith('• ') || line.startsWith('- ')) {
    const content = line.replace(/^[•-]\s+/, '');
    return `<li class="ml-6 mb-3 text-gray-300">${content}</li>`;
  }

  // Handle indented bullet points
  if (line.trim().startsWith('- ')) {
    const content = line.trim().replace(/^-\s+/, '');
    return `<li class="ml-10 mb-3 text-gray-300">${content}</li>`;
  }

  // Handle STAR format improvements
  if (line.includes('Original:')) {
    return `<div class="mb-3">
              <h4 class="text-lg font-semibold text-futuristic-accent mb-2">Original:</h4>
              <p class="text-gray-300 ml-4">${line.replace('Original:', '').trim()}</p>
            </div>`;
  }
  if (line.includes('→ Improved:')) {
    return `<div class="mb-6">
              <h4 class="text-lg font-semibold text-futuristic-accent mb-2">Improved Version:</h4>
              <p class="text-gray-300 ml-4">${line.replace('→ Improved:', '').trim()}</p>
            </div>`;
  }

  // Handle empty lines
  if (line.trim() === '') {
    return '<div class="h-4"></div>';
  }

  // Regular paragraphs
  return `<p class="mb-4 text-gray-300">${line}</p>`;
};

export default TextFormatter; 