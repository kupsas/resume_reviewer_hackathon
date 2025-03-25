import React from 'react';
import { cn } from '@/lib/utils';
import { Check, X, Lightbulb, Copy, CheckCircle2 } from 'lucide-react';

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
    improvement?: string;
    className?: string;
}

const StarAnalysisCard: React.FC<StarAnalysisCardProps> = ({
    text,
    star,
    metrics = [],
    improvement,
    className
}) => {
    const [copied, setCopied] = React.useState(false);

    const handleCopy = async () => {
        if (improvement) {
            await navigator.clipboard.writeText(improvement);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

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
                                        {value ? <Check className="h-4 w-4" /> : <X className="h-4 w-4" />}
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

                {/* Improvement */}
                {improvement && (
                    <div className="mt-4 p-3 bg-primary/5 dark:bg-primary/20 rounded-lg border border-primary/10 dark:border-primary/30">
                        <div className="flex items-start justify-between gap-2">
                            <div className="flex items-start gap-2 flex-grow">
                                <Lightbulb className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                                <div>
                                    <h4 className="text-sm font-medium text-foreground mb-1 underline decoration-primary/30 underline-offset-4">Suggested:</h4>
                                    <p className="text-sm text-foreground dark:text-primary-foreground">{improvement}</p>
                                </div>
                            </div>
                            <button
                                onClick={handleCopy}
                                className="p-1 hover:bg-primary/10 rounded-md transition-colors"
                                title="Copy suggestion"
                            >
                                {copied ? 
                                    <CheckCircle2 className="h-4 w-4 text-success" /> : 
                                    <Copy className="h-4 w-4 text-primary" />
                                }
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default StarAnalysisCard;
