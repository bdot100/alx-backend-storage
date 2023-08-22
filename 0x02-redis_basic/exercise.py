#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the input
data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str,
bytes, int or float.
"""
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    this method Counts the number of times a function
    is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    THis function counts the number of timesa 
    function is called
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


class Cache:
    """Redis Cache class"""
    def __init__(self) -> None:
        """
        This function initializes Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()
        
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string.
        The method should generate a random key
        (e.g. using uuid), store the input data in Redis
        using the random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


    @count_calls
    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        This function gets data from redis cache
        """
        retrievd_data = self._redis.get(key)
        if retrievd_data is not None and fn is not None and callable(fn):
            return fn(retrievd_data)
        return retrievd_data

    def get_str(self, key: str) -> str:
        """
        This function gets data as string from redis cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        This function gets data as integer from redis cache
        Args:
            key (str): key
        Returns:
            int: data
        """
        data = self
