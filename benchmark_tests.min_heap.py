import heapq
import timeit
import random
from min_heap import MinHeap

# Benchmark functions
def benchmark_custom_heap(n):
    values = [random.randint(0, 1000000) for _ in range(n)]
    heap = MinHeap()
    for v in values:
        heap.append(v)
    sorted_list = []
    while len(heap) > 0:
        sorted_list.append(heap.pop())
    return sorted_list

def benchmark_heapq(n):
    values = [random.randint(0, 1000000) for _ in range(n)]
    heap = []
    for v in values:
        heapq.heappush(heap, v)
    sorted_list = []
    while heap:
        sorted_list.append(heapq.heappop(heap))
    return sorted_list

if __name__ == '__main__':
    n = 10000  # Number of elements to use in each test
    repetitions = 10

    custom_time = timeit.timeit(lambda: benchmark_custom_heap(n), number=repetitions)
    heapq_time = timeit.timeit(lambda: benchmark_heapq(n), number=repetitions)

    print(f"Custom MinHeap total time over {repetitions} runs: {custom_time:.4f} seconds")
    print(f"heapq total time over {repetitions} runs: {heapq_time:.4f} seconds")