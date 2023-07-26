#!/usr/bin/python3
''' Basic dictionary'''
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    def __init__(self):
        self.cache_data = {}

    def put(self, key, item):
        if key:
            self.cache_data[key] = item

    def get(self, key):
        if key is None:
            return None
        return self.cache_data.get(key, None)
