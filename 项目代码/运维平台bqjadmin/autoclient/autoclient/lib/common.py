import time
import random
def unique_code():
    s = ''.join(random.sample(
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", ], 4))
    n=str(int(time.time()))
    return n+s