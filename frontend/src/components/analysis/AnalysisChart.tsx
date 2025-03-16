import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { motion } from 'framer-motion';

interface CategoryScore {
  name: string;
  score: number;
  maxScore: number;
  percentage: number;
  displayName?: string;
}

interface AnalysisChartProps {
  scores: CategoryScore[];
  title: string;
  id?: string;
}

const getBarColor = (percentage: number) => {
  if (percentage >= 80) return '#34D399'; // emerald-400
  if (percentage >= 60) return '#FBBF24'; // amber-400
  return '#F87171'; // red-400
};

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const scoreStatus = data.percentage >= 80 ? 'Excellent' : data.percentage >= 60 ? 'Good' : 'Needs Work';
    const scoreColor = data.percentage >= 80 ? 'text-emerald-400' : data.percentage >= 60 ? 'text-amber-400' : 'text-red-400';
    
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-700"
      >
        <p className="text-white font-semibold text-lg mb-3">{data.displayName}</p>
        <div className="space-y-3">
          <div className="flex items-center justify-between gap-4">
            <span className="text-gray-400">Score:</span>
            <span className="text-futuristic-accent font-medium">{data.score}/{data.maxScore}</span>
          </div>
          <div className="flex items-center justify-between gap-4">
            <span className="text-gray-400">Percentage:</span>
            <span className="text-futuristic-accent font-medium">{data.percentage.toFixed(1)}%</span>
          </div>
          <div className={`mt-3 px-3 py-1 rounded-full text-center text-sm font-medium ${scoreColor}`}>
            {scoreStatus}
          </div>
        </div>
      </motion.div>
    );
  }
  return null;
};

export const AnalysisChart: React.FC<AnalysisChartProps> = ({ scores, title, id }) => {
  if (scores.length === 0) {
    return null;
  }

  return (
    <motion.div
      id={id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mb-14 bg-gray-800 rounded-lg p-8 shadow-lg border border-gray-700"
    >
      <motion.h2
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-2xl font-semibold text-futuristic-accent mb-8 text-center"
      >
        {title}
      </motion.h2>
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={scores}
            layout="vertical"
            margin={{ top: 10, right: 50, left: 90, bottom: 10 }}
          >
            <XAxis 
              type="number" 
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
              tick={{ fill: '#9CA3AF', fontSize: 12 }}
            />
            <YAxis 
              type="category" 
              dataKey="displayName" 
              width={90}
              tick={{ 
                fill: '#9CA3AF', 
                fontSize: 13,
                textAnchor: 'end',
                dx: -10
              }}
            />
            <Tooltip 
              content={<CustomTooltip />}
              cursor={{ fill: 'rgba(75, 85, 99, 0.1)' }}
            />
            <Bar
              dataKey="percentage"
              radius={[0, 4, 4, 0]}
              barSize={24}
              animationDuration={1000}
              animationBegin={200}
            >
              {scores.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={getBarColor(entry.percentage)}
                >
                  <animate
                    attributeName="width"
                    from="0"
                    to={entry.percentage}
                    dur="1s"
                    fill="freeze"
                  />
                </Cell>
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
};

export default AnalysisChart; 