"""
Simple in-memory caching for capsule generation
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import json
from loguru import logger


class TTLCache:
    """Time-to-live cache with automatic expiration"""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache with TTL

        Args:
            ttl_seconds: Time to live in seconds (default: 1 hour)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def _generate_key(self, data: Dict[str, Any]) -> str:
        """Generate cache key from request data"""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True)
        return hashlib.md5(sorted_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self.cache:
            return None

        entry = self.cache[key]
        expires_at = entry.get("expires_at")

        if expires_at and datetime.now() > expires_at:
            # Expired, remove from cache
            del self.cache[key]
            logger.debug(f"Cache entry expired: {key}")
            return None

        logger.debug(f"Cache hit: {key}")
        return entry.get("value")

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with TTL"""
        expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
        self.cache[key] = {"value": value, "expires_at": expires_at}
        logger.debug(f"Cache set: {key} (expires at {expires_at})")

    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        logger.info("Cache cleared")

    def size(self) -> int:
        """Get number of cache entries"""
        return len(self.cache)


# Global cache instance
capsule_cache = TTLCache(ttl_seconds=3600)  # 1 hour TTL
