#!/usr/bin/env python3
"""
A module for a simple Cache class using Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be wrapped.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment the call count
        and call the original method.
        """
        key = method.__qualname__  # Use the qualified name as the key
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)  # Call the original method

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs and outputs
    for a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper to track the method's call history.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store inputs
        self._redis.rpush(input_key, str(args))

        # Execute the original method
        result = method(self, *args, **kwargs)

        # Store outputs
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


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

    @call_history
    @count_calls
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


def replay(method: Callable) -> None:
    """
    Display the history of calls to a method decorated with
    `count_calls` and `call_history`.

    Args:
        method (Callable): The method whose history to display.
    """
    # Access the Redis instance through the method's instance
    redis_instance = method.__self__._redis

    # Generate keys for call count, inputs, and outputs
    method_name = method.__qualname__
    call_count_key = f"{method_name}:calls"
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    # Fetch call count
    call_count = int(redis_instance.get(call_count_key) or 0)

    # Fetch inputs and outputs
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    # Display the results
    print(f"{method_name} was called {call_count} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")
