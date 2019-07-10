import asyncio
import random

# ANSI colors
c = (
    "\033[0m",  # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def makerandom(idx: int, threshold: int = 6):
    print(c[idx+1] + f"Initialized make random({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(f"makerandom({idx}) == {i} too low; retrying")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx+1]+f"---> finished makerandom({idx}) == {i}")
    return i


async def main():
    m, n = 10, 3
    assert(m != n)
    res = await asyncio.gather(*(makerandom(i, m - i - 1) for i in range(n)))
    return res


if __name__ == '__main__':
    random.seed(55)
    r1, r2, r3 = asyncio.run(main())
    print(f"\n r1: {r1}, r2: {r2}, r3: {r3}")
