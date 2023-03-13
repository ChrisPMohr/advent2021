from collections import Counter
counter = Counter(map(int, open('input.txt', 'r').readline().split(',')))
counts = [counter[k] for k in range(0, 9)]
for day in range(256):
    new_counts = counts[1:] + counts[:1]
    new_counts[6] += counts[0]
    counts = new_counts
print(sum(counts))