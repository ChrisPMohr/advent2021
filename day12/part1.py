from collections import defaultdict, Counter

def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    nodes = set()
    small_nodes = {'start', 'end'}
    edges = defaultdict(set)

    for line in lines:
        start, end = line.strip().split("-")
        nodes.add(start)
        nodes.add(end)
        edges[start].add(end)
        edges[end].add(start)
        if start not in {'start', 'end'} and start.lower() == start:
            small_nodes.add(start)
        if end not in {'start', 'end'} and end.lower() == end:
            small_nodes.add(end)

    num_paths = 0
    next_nodes = []
    for node in edges['start']:
        next_nodes.append((node, {'start', node}, ['start', node]))

    while next_nodes:
        next_node, path, real_path = next_nodes.pop(0)
        if next_node == 'end':
            print("Found real path", path, real_path)
            num_paths += 1
            continue

        for node in edges[next_node] - path.intersection(small_nodes):
            new_path = set(path)
            new_path.add(node)
            new_real_path = list(real_path)
            new_real_path.append(node)
            next_nodes.append((node, new_path, new_real_path))

    print(num_paths)


if __name__ == '__main__':
    main()