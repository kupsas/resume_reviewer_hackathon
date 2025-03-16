import React from 'react';

interface ScoreDisplayProps {
  score: number | null;
  isJobMatch: boolean;
}

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-emerald-400';
  if (score >= 60) return 'text-amber-400';
  return 'text-red-400';
};

export const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ score, isJobMatch }) => {
  if (score === null) return null;

  return (
    <div className="flex flex-col items-center justify-center mb-14">
      <h2 className="text-xl font-semibold text-gray-400 mb-4">
        {isJobMatch ? 'MATCH SCORE' : 'RESUME STRENGTH'}
      </h2>
      <div className={`text-8xl font-bold ${getScoreColor(score)} mb-2`}>
        {score}
      </div>
      <div className="flex gap-8 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-emerald-400 rounded"></div>
          <span className="text-gray-300 text-sm">Excellent (≥80)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-amber-400 rounded"></div>
          <span className="text-gray-300 text-sm">Good (60-79)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-red-400 rounded"></div>
          <span className="text-gray-300 text-sm">Needs Work (&lt;60)</span>
        </div>
      </div>
    </div>
  );
};

export default ScoreDisplay; 