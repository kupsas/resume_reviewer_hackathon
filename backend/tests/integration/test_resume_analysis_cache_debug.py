import pytest
from app.services.openai_service import OpenAIService
from app.services.cache import make_cache_key

@pytest.mark.asyncio
async def test_openai_service_cache_directly():
    """
    Direct test of OpenAIService cache without mocking.
    This will help us debug if the cache logic is working.
    """
    # Create a single OpenAI service instance
    service = OpenAIService()
    
    # Test data
    resume_text = "Test resume for cache debugging"
    
    # Check the cache key
    cache_key = make_cache_key(resume_text)
    print(f"Cache key: {cache_key}")
    
    # Check if cache is empty initially
    cached_result = service.cache.get(cache_key)
    print(f"Initial cache result: {cached_result}")
    assert cached_result is None, "Cache should be empty initially"
    
    # Manually set a value in cache
    test_value = {"test": "cached_value"}
    service.cache.set(cache_key, test_value)
    
    # Check if we can retrieve it
    cached_result = service.cache.get(cache_key)
    print(f"After set, cache result: {cached_result}")
    assert cached_result == test_value, "Cache should return the set value"
    
    print("✅ Cache is working correctly at the service level!")

if __name__ == "__main__":
    pytest.main([__file__]) 