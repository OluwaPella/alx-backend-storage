#!/usr/bin/env python3
"""
doc 
"""
import uuid
import redis
from typing import Union, Callable 
from functools  import wraps

def count_calls(method: Callable) -> Callable:
        """
        Decorator function that counts the number of calls made to a method.
        
        Parameters:
            method (function): The method to be decorated.

        Returns:
            function: The decorated method.

        """
        @wraps(method)
        def wrapper(self,  *args, **kwargs) -> any: 
            self._redis.incr(method.__qualname__)
            result = method(self, *args, **kwargs)
            return result
        return wrapper
def call_history(method: Callable) -> Callable:
        """
        Decorator function that stores the history of inputs and outputs for a method.

        Parameters:
            method (function): The method to be decorated.

        Returns:
            function: The decorated method.

        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input = str(args)
            self._redis.rpush(method.__qualname__ + ":inputs", input)
            output = str(method(self, *args, **kwargs))
            self._redis.rpush(method.__qualname__ + ":outputs", output)
            return output
        return wrapper

class Cache:

    def __init__(self):
        """
        Initializes a new instance of the Cache class.

        This constructor creates a new instance of the Cache class and initializes the `_redis` attribute with a new instance of the `redis.Redis` class. It also flushes the entire Redis database by calling the `flushdb()` method on the `_redis` object.

        Parameters:
            None

        Returns:
            None
        """
        self._redis = redis.Redis()
        self._redis.flushdb()
    @count_calls
    def store(self, data: Union[str, bytes, int, float ]) -> str:
        """doc method"""
        keyy = str(uuid.uuid4())
        self._redis.set(keyy, data)
        return keyy
    

    def get(self, key, fn=None):
        """
        Retrieves the value associated with the given key from the cache.

        Parameters:
            key (str): The key to retrieve the value for.
            fn (callable, optional): A function to apply to the retrieved value. Defaults to None.

        Returns:
            The value associated with the key, or the result of applying the function `fn` to the value if `fn` is provided. Returns None if the key does not exist in the cache.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        elif fn is None:
            return data
        else:
            return fn(data) 
    
    def get_str(self, key):
        """
        Retrieves the value associated with the given key from the cache and decodes it as a UTF-8 string.

        Parameters:
            key (str): The key to retrieve the value for.

        Returns:
            str: The decoded value associated with the key, or None if the key does not exist in the cache.
        """
        return self.get(key, lambda x: x.decode('utf-8'))
    def get_int(self,key):
        """
        Retrieves the value associated with the given key from the cache and converts it to an integer.

        Parameters:
            key (str): The key to retrieve the value for.

        Returns:
            int: The integer value associated with the key, or None if the key does not exist in the cache.
        """
        return self.get(key, lambda x: int(x))

