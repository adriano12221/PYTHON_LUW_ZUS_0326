import multiprocessing
import time

def compute(x):
    total = 0
    for i in range(10_000_000):
        total += x * i
    return total

if __name__ == '__main__':
    start = time.perf_counter()
    with multiprocessing.Pool(4) as pool:
        results = pool.map(compute, [1,2,3,4,5,6,7])
    end = time.perf_counter()
    print(f"Time taken: {end - start}s")
    print(results)

    print("______________")
    res = []
    start = time.perf_counter()
    for x in [1,2,3,4,5,6,7]:
        res.append(compute(x))
    end = time.perf_counter()
    print(f"Time taken: {end - start}s")
    print(res)
