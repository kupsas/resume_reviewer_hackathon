import React from 'react';
import { cn } from '@/lib/utils';
import { Check, X } from 'lucide-react';

interface StarAnalysis {
    situation: boolean;
    task: boolean;
    action: boolean;
    result: boolean;
    complete: boolean;
}

interface StarAnalysisCardProps {
    text: string;
    star: StarAnalysis;
    metrics?: string[];
    className?: string;
}

const StarAnalysisCard: React.FC<StarAnalysisCardProps> = ({
    text,
    star,
    metrics = [],
    className
}) => {
    return (
        <div className={cn("rounded-lg border p-4", className)}>
            <div className="space-y-4">
                {/* Text */}
                <div>
                    <p className="text-sm">{text}</p>
                </div>

                {/* STAR Analysis */}
                <div>
                    <h4 className="text-sm font-medium text-muted-foreground mb-2">STAR Analysis</h4>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        {Object.entries(star)
                            .filter(([key]) => key !== 'complete')
                            .map(([key, value]) => (
                                <div key={key} className="flex flex-col items-center">
                                    <span className="text-xs font-medium text-muted-foreground capitalize mb-1">
                                        {key}
                                    </span>
                                    <div className={cn(
                                        "w-6 h-6 rounded-full flex items-center justify-center",
                                        value ? "bg-success text-success-foreground" : "bg-muted text-muted-foreground"
                                    )}>
                                        {value ? "✓" : "×"}
                                    </div>
                                </div>
                            ))}
                    </div>
                </div>

                {/* Metrics */}
                {metrics.length > 0 && (
                    <div>
                        <h4 className="text-sm font-medium text-muted-foreground mb-2">Metrics</h4>
                        <div className="flex flex-wrap gap-2">
                            {metrics.map((metric, index) => (
                                <span key={index} className="chip bg-secondary text-secondary-foreground">
                                    {metric}
                                </span>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default StarAnalysisCard;
