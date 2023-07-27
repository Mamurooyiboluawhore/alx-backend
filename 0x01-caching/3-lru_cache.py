#!/usr/bin/python3
''' LRU Caching'''
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        ''' '''
        if key is None and item is None:
            return
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru, _ = self.cache_data.popitem(last=False)
            print("DISCARD:", lru)
        self.cache_data[key] = item

    def get(self, key):
        ''' gets data from cache'''
        return self.cache_data.get(key, None)
