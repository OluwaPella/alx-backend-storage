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
    def store(self, data: Union[str, bytes, int, float ]) -> str:
        """doc method"""
        keyy = str(uuid.uuid4())
        self._redis.set(keyy, data)
        return keyy
    
    def get(self, key, fn=None):
        data = self._redis.get(key)
        if data is None:
            return None
        elif fn is None:
            return data
        else:
            return fn(data) 
    
    def get_str(self, key):
        return self.get(key, lambda x: x.decode('utf-8'))
    def get_int(self,key):
        return self.get(key, lambda x: int(x)) 