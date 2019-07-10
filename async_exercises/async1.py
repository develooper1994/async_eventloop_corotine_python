#!/usr/bin/env python3
# countasync.py

import asyncio
import time


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def saysome(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def nested(): return 999


async def main():
    # async def saysome(delay, what)
    await saysome(1,"Selçuk")
    await saysome(1, "Çağlar")

    # create_task
    task1 = asyncio.create_task(saysome(1,'high'))
    task2 = asyncio.create_task(saysome(1,'way'))
    await task1
    await task2

    # tasks
    task3 = asyncio.create_task(saysome(1,"Wheeee!"))
    await task3

    # awaitable
    nested()  # not await then it won't run at all
    await nested()

    # if your function return value
    # async def count()
    await asyncio.gather(count(), count(), count())





if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main()) # run async function
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")