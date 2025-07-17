import time
import pytest
from app.services.cache import InMemoryCache, make_cache_key

def test_inmemory_cache_basic():
    """Test basic set/get functionality of InMemoryCache."""
    cache = InMemoryCache()
    key = make_cache_key("resume text 1")
    value = {"result": 123}
    assert cache.get(key) is None, "Cache should miss on first get"
    cache.set(key, value, ttl=5)
    assert cache.get(key) == value, "Cache should hit after set"


def test_inmemory_cache_ttl():
    """Test TTL expiration in InMemoryCache."""
    cache = InMemoryCache()
    key = make_cache_key("resume text 2")
    value = {"result": 456}
    cache.set(key, value, ttl=1)
    assert cache.get(key) == value, "Cache should hit before TTL expires"
    time.sleep(1.1)
    assert cache.get(key) is None, "Cache should miss after TTL expires"


def test_make_cache_key_uniqueness():
    """Test that different resume texts produce different cache keys."""
    key1 = make_cache_key("resume text 1")
    key2 = make_cache_key("resume text 2")
    assert key1 != key2, "Different texts should have different cache keys"
    assert isinstance(key1, str) and isinstance(key2, str), "Cache keys should be strings"


def test_make_cache_key_consistency():
    """Test that the same resume text always produces the same cache key."""
    text = "same resume text"
    key1 = make_cache_key(text)
    key2 = make_cache_key(text)
    assert key1 == key2, "Same text should always produce the same cache key"

if __name__ == "__main__":
    pytest.main([__file__]) 