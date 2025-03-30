import timeit
import random
import time
import matplotlib.pyplot as plt
from functools import lru_cache
from splay_tree import SplayTree

class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return None

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

    def invalidate(self, index):
        keys_to_delete = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_delete:
            node = self.cache[key]
            self.list.remove(node)
            del self.cache[key]

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R, lru_cache):
    key = (L, R)
    cached = lru_cache.get(key)
    if cached is not None:
        return cached
    else:
        result = sum(array[L:R+1])
        lru_cache.put(key, result)
        return result

def update_with_cache(array, index, value, lru_cache):
    array[index] = value
    lru_cache.invalidate(index)

@lru_cache(maxsize=1000)
def fibonacci_lru(n):
    if n <= 1:
        return n
    else:
        return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    else:
        cached = tree.find(n)
        if cached is not None:
            return cached
        else:
            res = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
            tree.insert(n, res)
            return res

def run_scenario_comparison():
    N = 100_000
    Q = 50_000
    array_no_cache = [random.randint(1, N) for _ in range(N)]
    array_with_cache = array_no_cache.copy()

    queries = []
    for _ in range(Q):
        if random.random() < 0.5:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, N)
            queries.append(('Update', index, value))

    lru_cache = LRUCache(capacity=1000)

    # Measure time without cache
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            _ = range_sum_no_cache(array_no_cache, query[1], query[2])
        else:
            update_no_cache(array_no_cache, query[1], query[2])
    time_no_cache = time.time() - start

    # Reset cache before testing with cache
    lru_cache = LRUCache(capacity=1000)

    # Measure time with cache
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            _ = range_sum_with_cache(array_with_cache, query[1], query[2], lru_cache)
        else:
            update_with_cache(array_with_cache, query[1], query[2], lru_cache)
    time_with_cache = time.time() - start

    print(f"Execution time without caching: {time_no_cache:.2f} seconds")
    print(f"Execution time with LRU-cache: {time_with_cache:.2f} seconds")


def build_demonstration():
    values_to_test = list(range(0, 1000, 50))

    lru_times = []
    splay_times = []

    for value in values_to_test:
        # LRU cache
        t_lru = timeit.timeit(lambda: fibonacci_lru(value), number=100)
        avg_lru = t_lru / 100
        lru_times.append(avg_lru)

        # Splay Tree
        splay_tree = SplayTree()
        t_splay = timeit.timeit(lambda: fibonacci_splay(value, splay_tree), number=100)
        avg_splay = t_splay / 100
        splay_times.append(avg_splay)

    # print results
    print("n         LRU Cache Time (s)  Splay Tree Time (s)")
    print("--------------------------------------------------")
    for i, n_val in enumerate(values_to_test):
        print(f"{n_val:<10}{lru_times[i]:<20.9f}{splay_times[i]:<20.9f}")

    # plot results
    plt.figure(figsize=(8, 5))
    plt.plot(values_to_test, lru_times, marker='o', label='LRU Cache')
    plt.plot(values_to_test, splay_times, marker='x', label='Splay Tree')
    plt.title('LRU Cache and Splay Tree execution time comparison')
    plt.xlabel('Fibonacci number (n)')
    plt.ylabel('Average execution time (s)')
    plt.legend()
    plt.grid(True)
    plt.show()