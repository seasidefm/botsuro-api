"""
Cache service
"""
import functools
import logging
import os
import pickle

import redis


def get_cache():
    """
    Get a cache instance
    :return:
    """
    return Cache(
        redis_string=os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )


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
        cached_data = self.redis.get(key)
        if cached_data:
            return pickle.loads(cached_data)
        return None

    def set(self, key: str, value, cache_time: int = 15 * 60):
        """
        Set the value of a key in the cache.

        :param key: The key of the data to be cached.
        :type key: str
        :param value: The value to be cached.
        :param cache_time: The time in seconds until the cache expires. Default is 15 minutes (900 seconds).
        :type cache_time: int
        :return: None
        """
        pickled_value = pickle.dumps(value)
        self.redis.set(key, pickled_value)
        self.redis.expire(key, cache_time)

    @staticmethod
    def cached_function(function, *args, key_prefix="", cache_time=15 * 60):
        cache = get_cache()

        prefix = key_prefix if key_prefix is not None else function.__name__
        cache_key = prefix + ":".join(map(str, args))
        cached_result = cache.get(cache_key)

        if cached_result is not None:
            return cached_result
        else:
            result = function(*args)
            cache.set(cache_key, result, cache_time)
            return result


def cached(cache: Cache = get_cache(), arg_key="key_arg", cache_time=15 * 60, namespace="default"):
    """
    Decorator that caches the result of a function based on arguments using a cache object.

    :param cache: Cache object to use for storing the cached result. Default is a configured redis cache object.
    :param arg_key: Key argument used to identify the cached result. Default is "key_arg".
    :param cache_time: Time in seconds to cache the result. Default is 15 minutes.
    :param namespace: Namespace to use for storing the cached result. Default is "default".
    :return: Decorated function that either returns the cached result or calls the original function and caches the result.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the cache key argument is present
            if arg_key in kwargs:
                key = str(kwargs[arg_key])

                cached_result = cache.get(key)
                if cached_result is not None:
                    print(f'Using cached result for argument {key}')
                    return cached_result

                # Call the function and cache the result
                result = func(*args, **kwargs)
                print(f'Caching result for argument {key}')
                cache.set(f"{namespace}:{key}", str(result), cache_time)
                return result

            # Else, just call the function
            logging.warning('No cache key argument %s found!', arg_key)
            return func(*args, **kwargs)

        return wrapper

    return decorator
