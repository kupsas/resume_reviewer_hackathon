'use client';

interface AnalysisResultsProps {
  analysis: {
    status: string;
    analysis: string;
  };
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysis }) => {
  // Convert the analysis string to HTML with proper formatting
  const formattedAnalysis = analysis.analysis
    .split('\n')
    .map((line) => {
      // Handle headers (lines starting with #)
      if (line.startsWith('# ')) {
        return `<h2 class="text-2xl font-bold text-blue-400 mt-6 mb-4">${line.replace('# ', '')}</h2>`;
      }
      // Handle subheaders (lines starting with ##)
      if (line.startsWith('## ')) {
        return `<h3 class="text-xl font-semibold text-blue-300 mt-4 mb-3">${line.replace('## ', '')}</h3>`;
      }
      // Handle bullet points
      if (line.startsWith('- ')) {
        return `<li class="ml-4 mb-2">${line.replace('- ', '')}</li>`;
      }
      // Handle empty lines
      if (line.trim() === '') {
        return '<br/>';
      }
      // Regular paragraphs
      return `<p class="mb-3">${line}</p>`;
    })
    .join('');

  return (
    <div className="bg-gray-800 rounded-lg p-8 shadow-lg border border-gray-700">
      <h2 className="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
        Resume Analysis Results
      </h2>
      
      <div className="prose prose-invert prose-lg max-w-none">
        <div 
          dangerouslySetInnerHTML={{ __html: formattedAnalysis }}
          className="space-y-2"
        />
      </div>
      
      <div className="mt-8 pt-6 border-t border-gray-700">
        <p className="text-sm text-gray-400">
          Analysis powered by OpenAI GPT-4
        </p>
      </div>
    </div>
  );
};

export default AnalysisResults; 