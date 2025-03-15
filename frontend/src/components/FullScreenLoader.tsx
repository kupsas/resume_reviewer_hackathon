'use client';

const FullScreenLoader = () => {
  return (
    <div className="fixed inset-0 bg-gray-900/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-8 max-w-md w-full mx-4 shadow-xl border border-gray-700">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
            <div className="absolute inset-0 w-16 h-16 border-4 border-purple-400 border-b-transparent rounded-full animate-spin-slow"></div>
          </div>
          
          <div className="text-center">
            <h3 className="text-xl font-semibold text-blue-400 mb-2">
              Analyzing Your Resume
            </h3>
            <p className="text-gray-400">
              Our AI is reviewing your resume and preparing detailed feedback...
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FullScreenLoader; 