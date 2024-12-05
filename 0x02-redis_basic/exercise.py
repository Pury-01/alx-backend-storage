#!/usr/bin/env python3
"""
A module for a simple Cache class using Redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class to interract with with a Redis instance.
    """

    def __init__(self):
        """
        Initiate the Cache instance   with a Redis client
        and flush it.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
         Store data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The randomly generated key.
        """
        key = str(uuid.uuid4())  # Generate a random UUID as the key
        self._redis.set(key, data)  # Store the data in Redis
        return key
