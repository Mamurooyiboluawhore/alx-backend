#!/usr/bin/env python3
''' Basic dictionary'''
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    ''' Basic cache class '''

    def put(self, key, item):
        ''' Assign the value to the key in dictionary if key is not None '''
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        ''' If key is None or if key doesn't exist in cache_data return None'''
        return self.cache_data.get(key, None)
