#!/usr/bin/env python3
"""
A module for a simple Cache class using Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional


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
            data (Union[str, bytes, int, float]): The data
            to store in Redis.

        Returns:
            str: The randomly generated key.
        """
        key = str(uuid.uuid4())  # Generate a random UUID as the key
        self._redis.set(key, data)  # Store the data in Redis
        return key

    def get(
            self, key: str,
            fn: Optional[
                Callable[
                    [bytes],
                    Union[str, int, bytes, float]
                    ]
                ] = None
    ) -> Union[str, int, bytes, None]:
        """
        Retrieve data from Redis by key and optionally
        transform it using fn.

        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable]): A callable function
            to transform the data.

        Returns:
            Union[str, int, bytes, None]: The retrieved data
            transformed if fn is provided.
        """
        value = self._redis.get(key)  # Retrieve the value from Redis
        if value is None:  # Key does not exist
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis by key.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[str]: The retrieved string or None
            if the key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis by key.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[int]: The retrieved integer or
            None if the key doesn't exist.
        """
        return self.get(key, fn=int)
