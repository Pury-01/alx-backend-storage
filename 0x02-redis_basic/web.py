#!/usr/bin/env python3
"""
implementing an expiring web cache and tracker
"""
import redis
import requests
from typing import Callable


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches it in Redis
    with an expiration time of 10 seconds.

    Also tracks how many times the URL has been accessed.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    # Initialize Redis connection
    redis_client = redis.Redis()

    # Track access count for the URL
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    # Cache key for the URL content
    cache_key = f"cached:{url}"
    cached_content = redis_client.get(cache_key)

    if cached_content:
        # If content is cached, return it
        return cached_content.decode('utf-8')

    # Fetch content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the content with a 10-second expiration time
    redis_client.setex(cache_key, 10, html_content)

    return html_content
