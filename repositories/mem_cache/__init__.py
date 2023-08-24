import os

import redis


class MemCache:
    """
    Cache service

    This class provides a cache service that uses Redis as the underlying caching mechanism. It allows for storing and retrieving data from the cache.

    Example usage:
    ```
    cache = MemCache("redis://localhost:6379/0")

    # Get a value from the cache
    value = cache.get("key")

    # Set a value in the cache
    cache.set("key", "value")
    ```

    Methods:
        - `__new__(cls, *args, **kwargs)`: This method is responsible for ensuring that only one instance of the class is created.
        - `__init__(self, redis_string: str)`: Initializes the MemCache instance with the Redis connection string.
        - `from_env(cls)`: Creates a MemCache instance using the Redis connection URL specified in the environment variable "REDIS_URL", or falls back to "redis://localhost:6379/0".
        - `get(self, key: str) -> bytes|None`: Retrieves the value associated with the given key from the cache. Returns `None` if the key does not exist in the cache, or the value if found.
        - `set(self, key: str, value: str, cache_time: int = 15 * 60) -> None`: Sets the value of a key in the cache with an optional expiration time. The default cache time is 15 minutes (900 seconds).

    Note:
        - The Redis connection URL should be in the format "redis://<host>:<port>/<db>".

    Example:
    ```python
    cache = MemCache.from_env()

    # Get a value from the cache
    value = cache.get("my_key")

    # Set a value in the cache with a custom expiration time of 1 hour (3600 seconds)
    cache.set("my_key", "my_value", 3600)
    ```
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MemCache, cls).__new__(cls)

        return cls._instance

    def __init__(self, redis_string: str):
        self.redis = redis.Redis.from_url(redis_string)

    @classmethod
    def from_env(cls):
        return MemCache(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

    def get(self, key: str):
        """
        Get a value from the cache
        :param key:
        :return:
        """
        return self.redis.get(key)

    def set(self, key: str, value: str, cache_time: int = 15 * 60):
        """
        Set the value of a key in the cache.

        :param key: The key of the data to be cached.
        :type key: str
        :param value: The value to be cached.
        :type value: str
        :param cache_time: The time in seconds until the cache expires. Default is 15 minutes (900 seconds).
        :type cache_time: int
        :return: None
        """
        self.redis.set(key, value)
        self.redis.expire(key, cache_time)
