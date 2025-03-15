'use client';

import { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/TextLayer.css';
import 'react-pdf/dist/Page/AnnotationLayer.css';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

interface SideByViewProps {
  resumeFile: File | null;
  analysis: {
    status: string;
    analysis: string;
  } | null;
}

interface Section {
  title: string;
  content: string;
  highlightArea?: {
    pageIndex: number;
    top: number;
    left: number;
    width: number;
    height: number;
  };
}

export default function SideByView({ resumeFile, analysis }: SideByViewProps) {
  const [numPages, setNumPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [scale, setScale] = useState<number>(1.2);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  // Convert file to URL for react-pdf
  const fileUrl = resumeFile ? URL.createObjectURL(resumeFile) : null;

  // Parse analysis into sections
  const sections: Section[] = analysis?.analysis.split('\n\n').map(section => {
    const [title, ...content] = section.split('\n');
    return {
      title: title.trim(),
      content: content.join('\n').trim(),
    };
  }) || [];

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages);
  }

  return (
    <div className="flex min-h-screen gap-4 p-4">
      {/* Left Sidebar - Analysis */}
      <div className="w-1/4 bg-futuristic-dark rounded-lg p-4 overflow-y-auto">
        <h2 className="text-xl font-semibold text-futuristic-accent mb-4">Analysis Overview</h2>
        <div className="space-y-4">
          {sections.map((section, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg transition-all cursor-pointer
                ${activeSection === section.title 
                  ? 'bg-futuristic-accent/20 border border-futuristic-accent' 
                  : 'bg-futuristic-light/10 hover:bg-futuristic-light/20'}`}
              onClick={() => setActiveSection(section.title)}
            >
              <h3 className="text-lg font-semibold text-futuristic-accent mb-2">
                {section.title}
              </h3>
              <div className="prose prose-sm prose-invert max-w-none">
                {section.content.split('\n').map((line, lineIndex) => (
                  line.startsWith('- ') ? (
                    <div key={lineIndex} className="flex items-baseline gap-2 mb-1">
                      <div className="w-1.5 h-1.5 bg-futuristic-accent/70 rounded-full mt-2"></div>
                      <p className="text-gray-300">{line.substring(2)}</p>
                    </div>
                  ) : (
                    <p key={lineIndex} className="text-gray-300 mb-1">{line}</p>
                  )
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Center - PDF Viewer */}
      <div className="flex-1 flex flex-col items-center bg-futuristic-dark rounded-lg p-4">
        <div className="flex gap-4 mb-4">
          <button
            onClick={() => setScale(prev => Math.max(0.5, prev - 0.1))}
            className="px-4 py-2 bg-futuristic-light rounded-md text-sm font-medium
              hover:bg-futuristic-light/80 transition-colors duration-200"
          >
            Zoom Out
          </button>
          <button
            onClick={() => setScale(prev => Math.min(2, prev + 0.1))}
            className="px-4 py-2 bg-futuristic-light rounded-md text-sm font-medium
              hover:bg-futuristic-light/80 transition-colors duration-200"
          >
            Zoom In
          </button>
          {numPages > 1 && (
            <div className="flex gap-2 items-center">
              <button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="px-4 py-2 bg-futuristic-light rounded-md text-sm font-medium
                  hover:bg-futuristic-light/80 transition-colors duration-200
                  disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="text-sm font-medium px-2">
                Page {currentPage} of {numPages}
              </span>
              <button
                onClick={() => setCurrentPage(prev => Math.min(numPages, prev + 1))}
                disabled={currentPage === numPages}
                className="px-4 py-2 bg-futuristic-light rounded-md text-sm font-medium
                  hover:bg-futuristic-light/80 transition-colors duration-200
                  disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          )}
        </div>

        <div className="relative bg-white rounded-lg shadow-xl">
          {fileUrl && (
            <Document
              file={fileUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              className="max-h-[calc(100vh-200px)] overflow-auto"
            >
              <Page
                pageNumber={currentPage}
                scale={scale}
                className="rounded-lg"
                renderAnnotationLayer={false}
                renderTextLayer={true}
              />
            </Document>
          )}
        </div>
      </div>

      {/* Right Sidebar - Section Details */}
      <div className="w-1/4 bg-futuristic-dark rounded-lg p-4 overflow-y-auto">
        <h2 className="text-xl font-semibold text-futuristic-accent mb-4">
          Detailed Analysis
        </h2>
        {activeSection ? (
          <div className="space-y-4">
            <div className="p-4 bg-futuristic-light/10 rounded-lg">
              <h3 className="text-lg font-semibold text-futuristic-accent mb-3">
                {activeSection}
              </h3>
              <div className="prose prose-sm prose-invert max-w-none">
                {sections
                  .find(s => s.title === activeSection)
                  ?.content.split('\n')
                  .map((line, index) => (
                    <p key={index} className="text-gray-300 mb-2 leading-relaxed">
                      {line}
                    </p>
                  ))}
              </div>
            </div>
          </div>
        ) : (
          <p className="text-gray-400 italic">Select a section to view detailed analysis</p>
        )}
      </div>
    </div>
  );
} 