"""
Cache service
"""
import redis


class Cache:
    """
    Cache service
    """
    def __init__(self, redis_string: str):
        self.redis = redis.Redis.from_url(redis_string)

    def get(self, key: str):
        """
        Get a value from the cache
        :param key:
        :return:
        """
        return self.redis.get(key)

    def set(self, key: str, value: str):
        """
        Set a value in the cache
        :param key:
        :param value:
        :return:
        """
        return self.redis.set(key, value)
