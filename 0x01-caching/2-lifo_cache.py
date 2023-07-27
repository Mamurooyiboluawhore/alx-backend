#!/usr/bin/python3
''' FIFO caching'''
from base_caching import BaseCaching
from collections import OrderedDict


class LIFOCache(BaseCaching):
    ''' Fifo cache'''
    def __init__(self):
        ''' Call the __init__ method of the parent class using super()'''
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        ''' add an item to the cache'''
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                newest_key, _ = self.cache_data.popitem(True)
                print("DISCARD:", newest_key)
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        ''' get data from cache'''
        return self.cache_data.get(key, None)
