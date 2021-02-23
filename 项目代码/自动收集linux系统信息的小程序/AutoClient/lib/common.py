#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author qiqiYang


def Bytes_MB(num,default=0):
    try:
        num=int(num)
        num=num/1024/1024
        num = round(num, 2)
    except Exception as e:
        num=default
    return num

def Bytes_KB(num,default=0):
    try:
        num=int(num)
        num=num//1024
    except Exception as e:
        num=default
    return num

def Bytes_GB(num,default=0):
    try:
        num=int(num)
        num=num//1024//1024//1024
    except Exception as e:
        num=default
    return num

def ms_s(num,default=0):
    try:
        num=int(num)
        num=num//1000
    except Exception as e:
        num=default
    return num

import time
import random
def unique_code():
    s = ''.join(random.sample(
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", ], 4))
    n=str(int(time.time()))
    return n+s
