from collections import deque
from itertools import groupby

# Cache Configuration
CACHE_SIZE = 64       # total number of cache blocks
BLOCK_SIZE = 1        # size of each block in words
TRACE_FILE = "memory_trace.txt"  # memory trace file to read

# Load memory addresses from the trace file
def load_trace(filename):
    with open(filename, 'r') as f:
        return [int(line.strip(), 16) for line in f if line.strip()]

# Simulate cache behavior with given associativity
def simulate_cache(trace, associativity=1):
    num_sets = CACHE_SIZE // associativity  # number of sets in the cache
    cache = [deque(maxlen=associativity) for _ in range(num_sets)]  # initialize cache
    hits = 0
    misses = 0

    for address in trace:
        block_address = address // BLOCK_SIZE
        index = block_address % num_sets  # find cache set index
        tag = block_address // num_sets   # compute tag

        if tag in cache[index]:  # if tag is in cache (hit)
            hits += 1
            cache[index].remove(tag)
            cache[index].append(tag)  # update for LRU
        else:  # miss
            misses += 1
            cache[index].append(tag)

    total = hits + misses
    hit_rate = hits / total * 100
    miss_rate = misses / total * 100
    return hits, misses, hit_rate, miss_rate

# Add some repeated addresses to improve temporal locality
def optimize_trace(trace):
    return trace + trace[:5]

# Print results
def print_stats(hits, misses, hit_rate, miss_rate, label):
    print(f"\n--- {label} ---")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print(f"Miss Rate: {miss_rate:.2f}%")

# Main function to run simulations
def main():
    trace = load_trace(TRACE_FILE)

    # Direct-mapped cache (1-way)
    print("Using Direct-Mapped Cache (Associativity = 1)")
    hits, misses, hit_rate, miss_rate = simulate_cache(trace, associativity=1)
    print_stats(hits, misses, hit_rate, miss_rate, "Before Optimization")

    optimized_trace = optimize_trace(trace)
    hits, misses, hit_rate, miss_rate = simulate_cache(optimized_trace, associativity=1)
    print_stats(hits, misses, hit_rate, miss_rate, "After Optimization")

    # 2-way set-associative cache
    print("\nNow using 2-Way Set-Associative Cache (Associativity = 2)")
    hits, misses, hit_rate, miss_rate = simulate_cache(trace, associativity=2)
    print_stats(hits, misses, hit_rate, miss_rate, "Before Optimization")

    hits, misses, hit_rate, miss_rate = simulate_cache(optimized_trace, associativity=2)
    print_stats(hits, misses, hit_rate, miss_rate, "After Optimization")

# Run the program
if __name__ == "__main__":
    main()