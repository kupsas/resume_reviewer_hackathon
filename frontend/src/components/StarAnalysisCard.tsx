import React from 'react';
import { cn } from '@/lib/utils';
import { Check, X, Lightbulb, Copy, CheckCircle2 } from 'lucide-react';

interface StarAnalysis {
    situation: boolean;
    situation_rationale: string;
    action: boolean;
    action_rationale: string;
    result: boolean;
    result_rationale: string;
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
        <div className={cn("rounded-lg border p-3 sm:p-4", className)}>
            <div className="space-y-3 sm:space-y-4">
                {/* Text */}
                <div className="px-1">
                    <p className="text-sm sm:text-base font-medium leading-relaxed">{text}</p>
                </div>

                {/* STAR Analysis */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3">
                    {[
                        { key: 'situation', label: 'Situation' },
                        { key: 'action', label: 'Action' },
                        { key: 'result', label: 'Result' }
                    ].map(({ key, label }) => (
                        <div 
                            key={key} 
                            className={cn(
                                "rounded-lg p-2 sm:p-3",
                                star[key as keyof StarAnalysis] 
                                    ? "bg-success/10 border border-success/20" 
                                    : "bg-muted/50 border border-muted"
                            )}
                        >
                            <span className="text-xs sm:text-sm font-semibold text-foreground capitalize block mb-1 sm:mb-2">
                                {label}
                            </span>
                            <p className="text-xs text-muted-foreground">
                                {star[`${key}_rationale` as keyof StarAnalysis]}
                            </p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Metrics */}
            {metrics.length > 0 && (
                <div className="mt-3 sm:mt-4 px-1">
                    <h4 className="text-xs sm:text-sm font-semibold text-foreground mb-2">Metrics</h4>
                    <div className="flex flex-wrap gap-1.5 sm:gap-2">
                        {metrics.map((metric, index) => (
                            <span key={index} className="inline-flex px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-md bg-secondary text-xs font-medium text-secondary-foreground">
                                {metric}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Improvement */}
            {improvement && (
                <div className="mt-3 sm:mt-4 p-2 sm:p-3 bg-primary/5 dark:bg-primary/20 rounded-lg border border-primary/10 dark:border-primary/30">
                    <div className="flex items-start justify-between gap-2">
                        <div className="flex items-start gap-2 flex-grow">
                            <Lightbulb className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                            <div>
                                <h4 className="text-xs sm:text-sm font-medium text-foreground mb-1 underline decoration-primary/30 underline-offset-4">Suggested:</h4>
                                <p className="text-xs sm:text-sm text-foreground dark:text-primary-foreground">{improvement}</p>
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
    );
};

export default StarAnalysisCard;
