import json
import time
import hashlib
import logging
from typing import Any, Optional
import os
from urllib.parse import urlparse
import redis  # Add the redis import

logger = logging.getLogger(__name__)

class CacheBase:
    """
    Abstract base class for cache implementations.
    Defines the interface for get, set, and clear methods.
    """
    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def set(self, key: str, value: Any, ttl: int = 86400) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

class InMemoryCache(CacheBase):
    """
    Simple in-memory cache using a Python dict with TTL (time-to-live) support.
    For development and testing only. Not suitable for production.
    """
    def __init__(self):
        # Store values as {key: (value, expire_time)}
        self._store = {}
        logger.info("InMemoryCache initialized (dev mode)")

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry:
            value, expire_time = entry
            if expire_time is None or expire_time > time.time():
                logger.info(f"[CACHE HIT] InMemoryCache for key: {key}")
                return value
            else:
                logger.info(f"[CACHE EXPIRED] InMemoryCache for key: {key}")
                del self._store[key]
        logger.info(f"[CACHE MISS] InMemoryCache for key: {key}")
        return None

    def set(self, key: str, value: Any, ttl: int = 86400) -> None:
        expire_time = time.time() + ttl if ttl else None
        self._store[key] = (value, expire_time)
        logger.info(f"[CACHE SET] InMemoryCache for key: {key} (ttl={ttl}s)")

    def clear(self) -> None:
        self._store.clear()
        logger.info("[CACHE CLEAR] InMemoryCache cleared")

class RedisCache(CacheBase):
    """
    Redis-backed cache for production use.
    Connects to a Redis server using environment variables for configuration.
    """
    def __init__(self):
        redis_url = os.getenv('REDIS_URL')
        if redis_url:
            # Parse the URL
            parsed = urlparse(redis_url)
            redis_host = parsed.hostname
            redis_port = parsed.port
            redis_password = parsed.password
            redis_db = int(parsed.path.lstrip('/')) if parsed.path else 0
        else:
            # Fallback to individual env vars
            redis_host = os.getenv('REDIS_HOST', 'localhost')
            redis_port = int(os.getenv('REDIS_PORT', 6379))
            redis_password = os.getenv('REDIS_PASSWORD', None)
            redis_db = int(os.getenv('REDIS_DB', 0))
        self.ttl = int(os.getenv('CACHE_TTL', 86400))
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
            decode_responses=True
        )
        logger.info(f"RedisCache initialized at {redis_host}:{redis_port} (db={redis_db})")

    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value is not None:
            logger.info(f"[CACHE HIT] RedisCache for key: {key}")
            return value
        else:
            logger.info(f"[CACHE MISS] RedisCache for key: {key}")
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        # Use provided TTL or default
        ttl = ttl if ttl is not None else self.ttl
        self.redis.setex(key, ttl, value)
        logger.info(f"[CACHE SET] RedisCache for key: {key} (ttl={ttl}s)")

    def clear(self) -> None:
        # WARNING: This will delete all keys in the current Redis DB!
        self.redis.flushdb()
        logger.info("[CACHE CLEAR] RedisCache cleared (all keys deleted)")

    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value is not None:
            logger.info(f"[CACHE HIT] RedisCache for key: {key}")
            try:
                # Try to parse JSON back to dict
                return json.loads(value)
            except Exception:
                # If not JSON, just return as is
                return value
        else:
            logger.info(f"[CACHE MISS] RedisCache for key: {key}")
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        ttl = ttl if ttl is not None else self.ttl
        # Serialize dicts to JSON before storing
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.redis.setex(key, ttl, value)
        logger.info(f"[CACHE SET] RedisCache for key: {key} (ttl={ttl}s)")

# Factory function to select cache backend based on environment variable

def get_cache_backend() -> CacheBase:
    """
    Returns the appropriate cache backend based on the USE_REDIS environment variable.
    If USE_REDIS is set to 'true', use RedisCache. Otherwise, use InMemoryCache.
    """
    use_redis = os.getenv('USE_REDIS', 'false').lower() == 'true'
    if use_redis:
        return RedisCache()
    else:
        return InMemoryCache()

def make_cache_key(resume_text: str) -> str:
    """
    Generate a cache key by hashing the resume text.
    This ensures that identical resumes map to the same cache entry.
    """
    return hashlib.sha256(resume_text.encode('utf-8')).hexdigest() 