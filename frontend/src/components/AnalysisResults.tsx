'use client';

interface AnalysisResultsProps {
  analysis: {
    status: string;
    analysis: string;
  };
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysis }) => {
  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-blue-400">Analysis Results</h2>
      <div className="prose prose-invert">
        <div dangerouslySetInnerHTML={{ __html: analysis.analysis }} />
      </div>
    </div>
  );
};

export default AnalysisResults; 