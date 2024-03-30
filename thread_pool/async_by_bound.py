from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
from os import getpid
import math
import time
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def elapsed(func):
    def wrap(*args):
        start_r = time.perf_counter()
        start_p = time.process_time()
        ret = func(*args)
        end_r = time.perf_counter()
        end_p = time.process_time()
        elapsed_r = end_r - start_r
        elapsed_p = end_p - start_p

        print(f'[{func.__name__}]\nelapsed: {elapsed_r:.6f}sec (real) / {elapsed_p:.6f}sec (cpu)')
        return ret
    # 함수 객체를 return
    return wrap

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

def open_file(filename):
    with open(filename, "r") as infile:
        lines = infile.readlines()
        # for line in lines:
        #     print(line)

@elapsed
def run_async_process_with_ProcessPoolExcutor(myFunc, dataList):
    '''[CPU Bound Process] Async Process Case 1: ProcessPoolExcutor")'''
    threads = []
    pool = ProcessPoolExecutor(max_workers=7)
    for prime in dataList:
        threads.append(pool.submit(myFunc, prime))
    wait(threads)

@elapsed
def run_async_process_with_ThreadPoolExcutor(myFunc, dataList):
    '''[CPU Bound Process] Async Process Case 2: ThreadPoolExcutor'''
    with ThreadPoolExecutor(max_workers=10000) as excutor:
        excutor.map(myFunc, dataList)
        # for number, prime in zip(dataList, excutor.map(is_prime, dataList)):
        #     print('%d is prime: %s' % (number, prime))

@elapsed
def run_sync_process(myFunc, dataList):
    # map(is_prime, dataList)
    for number, prime in zip(dataList, map(myFunc, dataList)):
        pass
        # print('%d is prime: %s' % (number, prime))

# NOTE: CPU bound 예시
def main():
    # myFunc = is_prime

    # run_async_process_with_ProcessPoolExcutor(myFunc, PRIMES)
    # print()
    # run_async_process_with_ThreadPoolExcutor(myFunc, PRIMES)
    # print()
    # run_sync_process(is_prime, PRIMES)

    myFunc = open_file
    file_name_list = ['test.txt' for i in range(3000)]
    run_async_process_with_ProcessPoolExcutor(myFunc, file_name_list)
    print()
    run_async_process_with_ThreadPoolExcutor(myFunc, file_name_list)
    print()
    run_sync_process(myFunc, file_name_list)




if __name__ == '__main__':
    main()
