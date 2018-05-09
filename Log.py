import sys

DEBUG = 0

def debug(a):
    if DEBUG:
        print(a)

def eprint(*args, **kwargs): # error print
    print(*args, file=sys.stderr, **kwargs)