#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from heapq import *

class hnode(object):
    def __init__(self, frequency, left=None, right=None):
        self.frequency = frequency
        self.left = left
        self.right = right

    # Custom comparison method for heap operations
    def __lt__(self, other):
        return self.frequency < other.frequency

def build(freq):
    queue = []
    for i in range(0, 256):
        if (freq[i] != 0):
            heappush(queue, (freq[i], hnode(frequency=freq[i], left=None, right=None)))  # Provide the frequency to hnode
    while (len(queue) > 1):
        a = heappop(queue)
        b = heappop(queue)
        freq_sum = a[0] + b[0]
        node = hnode(frequency=freq_sum, left=a[1], right=b[1])  # Provide the frequency to hnode
        heappush(queue, (freq_sum, node))
    return queue[0][1]  # Return the root of the Huffman tree

def walk(node, prefix="", code={}):
    if isinstance(node, hnode):  # Check if the node is an instance of hnode
        walk(node.left, prefix + "0", code)
        walk(node.right, prefix + "1", code)
    else:
        code[node] = prefix  # Use node directly as the key in the code dictionary
    return code

def huffman(lst):
    freq = [0] * 256
    for n in lst:
        freq[n] += 1

    htree = build(freq)
    code = {i: '' for i in range(256)}  # Initialize code dictionary with default empty strings

    walk(htree, code=code)  # Update the code dictionary

    return code
def encode(s, ch):
    while len(s) % 8 != 0:
        s += ch
    lst = []
    for i in range(0, len(s) // 8):
        n = 0
        for j in range(0, 8):
            k = i * 8 + j
            n |= (1 if (s[k] == ch) else 0) << (7 - j)  # Correctly calculate the value based on bit position
        lst.append(n)
    return lst, len(s) // 8  # Return the encoded list and the number of characters


def compress(content):
    fcount = int(len(content) / 80 / 25)  # Convert fcount to an integer
    edata, elen = encode(content, '*')
    code = huffman(edata)
    hdata = ""
    for item in edata:
        hdata += code[item]

    # Pad hdata to make its length a multiple of 8
    while len(hdata) % 8 != 0:
        hdata += '0'

    # Calculate the actual length of hdata after padding
    actual_hdata_length = len(hdata) // 8

    code_bytes = [
        fcount >> 8, fcount & 0xff, elen >> 24, (elen >> 16) & 0xff,
        (elen >> 8) & 0xff, elen & 0xff,
        actual_hdata_length  # Use the actual length of hdata in code_bytes
    ]

    for i in range(256):  # Add all possible characters to code_bytes, even if they have zero frequency
        if i in code:
            code_bytes.append(i)
            tmp = encode(code[i], '1')
            code_bytes.append(len(code[i]))
            code_bytes += tmp[0]  # Unpack the encoded list from the tuple and add it to code_bytes
        else:
            code_bytes.append(i)
            code_bytes.append(0)
            code_bytes.append(0)  # Add zero length for characters with zero frequency

    return code_bytes + encode(hdata, '1')[0]  # Unpack the encoded list from the tuple

# Rest of the code remains unchanged


# Rest of the code remains unchanged


# Rest of the code remains unchanged

if __name__ == "__main__":
  txt, bin = sys.argv[1], sys.argv[2]
  data = []

  with open(txt, "r") as fin:
    with open(bin, "wb") as fout:
      content = ''.join(fin.readlines())
      content = ''.join(content.splitlines())
      fout.write(bytearray(compress(content)))
