from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    polymer = list(lines[0].strip())
    rules = {}

    for line in lines[2:]:
        pair, out = line.strip().split(" -> ")
        rules[pair] = out

    for _ in range(10):
        new_polymer = []
        for char1, char2 in zip(polymer[:-1], polymer[1:]):
            new_polymer.append(char1)
            new_polymer.append(rules[char1 + char2])

        new_polymer.append(polymer[-1])
        print(new_polymer)
        polymer = new_polymer

    chars = Counter(polymer)
    sorted_map = sorted(list(chars.items()), key=lambda k: k[1])
    print(sorted_map)
    print(sorted_map[-1][1] - sorted_map[0][1])




    # items = {}
    # for y, line in enumerate(lines):
    #     for x, c in enumerate(line.strip()):
    #         items[(x, y)] = int(c)

    # max_x = max(x for x,y in items)
    # max_y = max(y for x,y in items)
    # for y in range(0, max_y + 1):
    #     print("".join('#' if (x,y) in items else ' ' for x in range(0, max_x+10)))

if __name__ == '__main__':
    main()