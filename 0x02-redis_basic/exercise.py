#!/usr/bin/env python3
"""
doc 
"""
import uuid
import redis
from typing import Union

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    def set(self, data: Union[str, bytes, int, float ]) -> str:
        keyy = str(uuid.uuid4())
        self._redis.set(keyy, data)
        return keyy 

