#!/usr/bin/env python3
""" Simple helper function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ Pagnation"""
    if page <= 1:
        start_index = 0
    else:
        start_index = (page - 1) * page_size
    # Calculate the starting and ending index of the page
    end_index = page * page_size
    return start_index, end_index
