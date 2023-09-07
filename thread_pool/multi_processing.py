from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
from multiprocessing import Pool
from os import getpid
import math
import time

# def double(i):
#     print("I'm processing ", getpid())
#     return i * 2

# with Pool() as pool:
#     result = pool.map(double, [1, 2, 3, 4, 5])
#     print(result)

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419
]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

# NOTE: CPU bound 예시
def main():
    # NOTE: 사용방법 1
    print("Async Process Case 1 [ProcessPoolExcutor]")
    start = time.time()
    threads = []
    pool = ProcessPoolExecutor(max_workers=7)
    for prime in PRIMES:
        threads.append(pool.submit(is_prime, prime))
    wait(threads)
    end = time.time()
    print('Running time:', f'{end - start}s')
    
    # NOTE: 사용방법 2
    print("Async Process Case 2 [ThreadPoolExcutor]")
    start = time.time()
    with ThreadPoolExecutor(max_workers=7) as excutor:
        for number, prime in zip(PRIMES, excutor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))
    end = time.time()
    print('Running time:', f'{end - start}s')

    print("Sync Process")
    start = time.time()
    for number, prime in zip(PRIMES, map(is_prime, PRIMES)):
        print('%d is prime: %s' % (number, prime))
    end = time.time()
    print('Running time:', f'{end - start}s')


if __name__ == '__main__':
    main()
