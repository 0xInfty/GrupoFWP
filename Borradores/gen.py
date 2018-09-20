# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 21:37:31 2018

@author: Marcos
"""

def yield_chunks(arr, chunk_size):
    larr = len(arr)
    if larr < chunk_size:
        raise ValueError("The array length (%d) must be larger than the chunk size (%d)" % (len(arr), chunk_size))

    cursor = 0
    while cursor < larr:
        next_cursor = min(cursor + chunk_size, larr)
        yield arr[cursor:next_cursor]
        cursor = next_cursor


def yield_chunks_forever(arr, chunk_size):
    while True:
        yield from yield_chunks(arr, chunk_size)

def yield_chunks_forever_mod(arr, chunk_size):
    while True:
        yield from yield_chunks(arr, chunk_size)
        yield 'a'
        arr = [2*x for x in arr]


def yield_chunks_repeat(arr, chunk_size, times):
    for n in range(times):
        yield from yield_chunks(arr, chunk_size)
        
        #%%
x = list(range(10))
print(list(yield_chunks(x, 3)))
print(list(yield_chunks(x, 2)))