"""
Tests for caching functionality
"""

import pytest
from datetime import datetime, timedelta
from app.services.cache import TTLCache, capsule_cache


class TestTTLCache:
    """Test TTL cache functionality"""

    def test_cache_set_get(self):
        """Test basic set and get"""
        cache = TTLCache(ttl_seconds=3600)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = TTLCache(ttl_seconds=3600)
        assert cache.get("nonexistent") is None

    def test_cache_expiration(self):
        """Test cache entries expire"""
        cache = TTLCache(ttl_seconds=1)  # 1 second TTL
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

        # Wait for expiration (in real test, use time mocking)
        import time

        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_cache_clear(self):
        """Test cache clearing"""
        cache = TTLCache(ttl_seconds=3600)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.size() == 2

        cache.clear()
        assert cache.size() == 0
        assert cache.get("key1") is None

    def test_cache_key_generation(self):
        """Test cache key generation is consistent"""
        cache = TTLCache()
        data1 = {"a": 1, "b": 2}
        data2 = {"b": 2, "a": 1}  # Same data, different order

        key1 = cache._generate_key(data1)
        key2 = cache._generate_key(data2)

        assert key1 == key2  # Should be same regardless of order

    def test_global_cache_instance(self):
        """Test global cache instance exists"""
        assert capsule_cache is not None
        assert isinstance(capsule_cache, TTLCache)
