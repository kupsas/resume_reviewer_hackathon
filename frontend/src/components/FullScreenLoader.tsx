'use client';

export default function FullScreenLoader() {
  return (
    <div className="fixed inset-0 bg-futuristic-dark/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="relative flex items-center justify-center">
        {/* Outer ring */}
        <div 
          className="absolute border-4 border-futuristic-accent/20 rounded-full animate-spin-slow"
          style={{ width: '120px', height: '120px' }}
        />
        
        {/* Middle ring */}
        <div 
          className="absolute border-4 border-t-futuristic-accent border-r-futuristic-accent/50 border-b-futuristic-accent/30 border-l-futuristic-accent/10 rounded-full animate-spin-reverse"
          style={{ width: '80px', height: '80px' }}
        />
        
        {/* Inner ring */}
        <div 
          className="absolute border-2 border-futuristic-accent/40 rounded-full animate-spin-slow"
          style={{ width: '50px', height: '50px' }}
        />
        
        {/* Center dot */}
        <div className="absolute w-4 h-4 bg-futuristic-accent rounded-full animate-pulse-glow" />
        
        {/* Loading text */}
        <div className="absolute -bottom-24 left-1/2 -translate-x-1/2 whitespace-nowrap text-center">
          <p className="text-futuristic-accent text-xl font-semibold mb-3">
            Analyzing Resume
          </p>
          <div className="flex justify-center gap-2">
            <div className="w-2 h-2 bg-futuristic-accent rounded-full animate-bounce" 
                 style={{ animationDelay: '0s' }} />
            <div className="w-2 h-2 bg-futuristic-accent rounded-full animate-bounce" 
                 style={{ animationDelay: '0.2s' }} />
            <div className="w-2 h-2 bg-futuristic-accent rounded-full animate-bounce" 
                 style={{ animationDelay: '0.4s' }} />
          </div>
        </div>
      </div>
    </div>
  );
} 