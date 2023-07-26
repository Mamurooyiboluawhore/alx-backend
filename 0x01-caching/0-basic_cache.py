#!/usr/bin/env python3
''' Basic dictionary'''
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    ''' Basic cache class '''
    def __init__(self):
        ''' Create an empty dictionary as an instance'''
        self.cache_data = {}

    def put(self, key, item):
        # Assign the value to the key in the dictionary if key is not None
        if key:
            self.cache_data[key] = item

    def get(self, key):
        # If key is None or if the key doesn't exist in cache_data, return None
        if key is None:
            return None
        return self.cache_data.get(key, None)
