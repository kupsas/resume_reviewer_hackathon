"""Test script for education section prompt development."""
import json
import asyncio
from openai import AsyncOpenAI
from app.core.config import settings

# Load sample data
with open("tests/data/sample_education_sections.json") as f:
    SAMPLE_DATA = json.load(f)

# Use the long prompt
SYSTEM_PROMPT = """You are an expert resume analyzer. Analyze the provided education section and return a JSON response.

For Education section:
- Extract and analyze:
  * Subject: The specific field of study (e.g., Computer Science, Business Administration)
  * Course: The type of degree or qualification (e.g., Bachelor of Science, MBA)
  * School: The educational institution name
- Evaluate institution reputation:
  * Domestic score (1-10) based on:
    - National rankings and academic excellence
    - Research output and impact
    - Industry connections and partnerships
    - Program-specific reputation
    - Alumni network strength
  * International score (1-10) based on:
    - Global university rankings
    - International research collaborations
    - Global recognition and partnerships
    - International student/faculty diversity
    - Cross-border academic programs
  * Provide detailed rationale for each score
- Include any additional details like GPA, relevant coursework, or achievements

Return analysis in JSON format following the specified schema."""

async def test_sample(sample: dict, client: AsyncOpenAI) -> dict:
    """Test a single sample with the system prompt."""
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": sample["text"]}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        result = json.loads(response.choices[0].message.content)
        return {
            "sample": sample["text"],
            "expected": sample["expected_output"],
            "actual": result,
            "matches": result == sample["expected_output"],
            "token_usage": {
                "total_tokens": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        }
    except Exception as e:
        return {
            "sample": sample["text"],
            "error": str(e)
        }

async def run_tests():
    """Run tests on all samples."""
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    results = []
    
    print("🧪 Starting education prompt tests...\n")
    print(f"Testing {len(SAMPLE_DATA['samples'])} samples with the long prompt.\n")
    
    for i, sample in enumerate(SAMPLE_DATA["samples"], 1):
        print(f"\n📝 Testing sample {i}/{len(SAMPLE_DATA['samples'])}...")
        print(f"Input text: {sample['text']}\n")
        
        result = await test_sample(sample, client)
        results.append(result)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("Response:")
            print(json.dumps(result["actual"], indent=2))
            print("\nToken Usage:")
            print(f"Total Tokens: {result['token_usage']['total_tokens']}")
            print(f"Prompt Tokens: {result['token_usage']['prompt_tokens']}")
            print(f"Completion Tokens: {result['token_usage']['completion_tokens']}")
            
            if result["matches"]:
                print("\n✅ Response matches expected output!")
            else:
                print("\n❌ Response differs from expected output:")
                print("Expected:", json.dumps(result["expected"], indent=2))
            
            print("\n" + "="*50)
    
    # Calculate statistics
    successful = sum(1 for r in results if "matches" in r and r["matches"])
    total = len(results)
    total_tokens = sum(r["token_usage"]["total_tokens"] for r in results if "token_usage" in r)
    
    print(f"\n📊 Test Results Summary:")
    print(f"Total samples: {total}")
    print(f"Successful matches: {successful}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    print(f"Total tokens consumed: {total_tokens}")
    print(f"Average tokens per sample: {total_tokens/total:.1f}")

if __name__ == "__main__":
    asyncio.run(run_tests()) 