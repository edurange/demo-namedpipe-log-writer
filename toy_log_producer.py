#!/usr/bin/env python3

"""
A simple continuous file writer

Uses time.sleep() to simulate work that is CPU-bound.
"""

from datetime import datetime
import sys
import time

__author__ = "Joe Granville"
__date__ = "20250526"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

DELAY = 3

if __name__ == "__main__":
    filepath = sys.argv[1]
    print("I'll write whenever I want, watch me")
    with open(filepath, "a", encoding="utf-8") as file:
        print(f'I opened "{filepath}" to append')
        while True:
            print(f"I wrote at {datetime.now()}")
            file.write(f"I'm writing at {datetime.now()}\n")
            file.flush()
            print(f"I finished writing at {datetime.now()}")
            print(f"Now I'll do something else for {DELAY} seconds")
            time.sleep(DELAY)
