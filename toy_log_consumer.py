#!/usr/bin/env python3

"""
A file reader to contrast the features of files and named pipes

Uses a thread to wrap the blocking IO in an awaitable and release the
Global Interpreter Lock. This is not a general endorsement of threading.
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import sys

__author__ = "Joe Granville"
__date__ = "20250526"
__license__ = "MIT"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"


@asynccontextmanager
async def asyncopen(path, mode):
    """
    Asynchronously waits for a file to open, then closes it
    """
    print(f'Opening "{path}"')
    file = await asyncio.to_thread(open, path, mode)
    print("foo")
    yield file
    print(f'Closing "{path}"')
    file.close()


async def coroutineread(path):
    """
    Asynchronously reads and prints lines as they become available
    
    Needs to detect when other writers close the pipe, otherwise reads
    will stop blocking and return empty strings indefinitely.
    """
    async with asyncopen(path, "rb") as file:
        print(f'I opened "{path}" to read')
        while True:
            print("I will not poll the filesystem")
            print(f"It's {datetime.now()} and I'm waiting to read")
            bytedata = await asyncio.to_thread(file.readline)
            line = bytedata.decode("utf-8")
            print(f'The producer wrote "{line.strip()}"')


DELAY = 5


async def busywork():
    """
    Simulate other work that is CPU-bound
    """
    while True:
        print(f"It's {datetime.now()}")
        print(f"I get other things done every {DELAY} seconds")
        await asyncio.sleep(DELAY)


async def tasks(path):
    """
    Runs coroutineread and busywork together concurrently
    """
    async with asyncio.TaskGroup() as tg:
        read = tg.create_task(coroutineread(path))
        work = tg.create_task(busywork())


if __name__ == "__main__":
    filepath = sys.argv[1]
    print(
        'Teacher made me write "I will not poll the filesystem" an '
        "indefinite number of times"
    )
    asyncio.run(tasks(filepath))
