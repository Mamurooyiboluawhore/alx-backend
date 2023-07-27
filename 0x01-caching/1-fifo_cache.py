#!/usr/bin/python3
''' FIFO caching'''
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    ''' Fifo cache'''
    def __init__(self):
        ''' Call the __init__ method of the parent class using super()'''
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        ''' add an item to the cache'''
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            oldest_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", oldest_key)

    def get(self, key):
        ''' get data from cache'''
        return self.cache_data.get(key, None)
