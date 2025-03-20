"""Token usage tracking and cost calculation utilities."""
from typing import Dict
from dataclasses import dataclass
from openai.types.completion_usage import CompletionUsage

@dataclass
class ModelPricing:
    """Pricing information for different models."""
    prompt_cost_per_1k: float
    completion_cost_per_1k: float

MODEL_PRICING = {
    "gpt-4-turbo-preview": ModelPricing(0.01, 0.03),  # $0.01 per 1K prompt, $0.03 per 1K completion
    "gpt-4o-mini-2024-07-18": ModelPricing(0.001, 0.002),  # Example pricing
    "gpt-3.5-turbo": ModelPricing(0.0005, 0.0015)  # Default GPT-3.5 pricing
}

class TokenUsageTracker:
    """Track token usage and calculate costs across different models."""
    
    def __init__(self):
        self.usage = {
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0
        }
    
    def update(self, usage: CompletionUsage, model: str) -> None:
        """Update token usage statistics based on the model used."""
        self.usage["total_tokens"] += usage.total_tokens
        self.usage["prompt_tokens"] += usage.prompt_tokens
        self.usage["completion_tokens"] += usage.completion_tokens
        
        # Get pricing for the model, default to GPT-3.5 if unknown
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-3.5-turbo"])
        
        # Calculate costs
        prompt_cost = (usage.prompt_tokens / 1000) * pricing.prompt_cost_per_1k
        completion_cost = (usage.completion_tokens / 1000) * pricing.completion_cost_per_1k
        
        self.usage["total_cost"] += prompt_cost + completion_cost
    
    def get_usage(self) -> Dict:
        """Get current token usage statistics."""
        return self.usage.copy()
