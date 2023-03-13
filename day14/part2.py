from collections import defaultdict, Counter


def main():
    lines = open('input.txt', 'r').readlines()

    polymer = list(lines[0].strip())
    polymer_tuples = Counter(zip(polymer[:-1], polymer[1:]))

    rules = {}
    for line in lines[2:]:
        pair, out = line.strip().split(" -> ")
        rules[tuple(pair)] = out

    for i in range(40):
        new_polymer_tuples = defaultdict(int)
        for (first, last), count in polymer_tuples.items():
            middle = rules[(first, last)]
            new_polymer_tuples[(first, middle)] += count
            new_polymer_tuples[(middle, last)] += count

        polymer_tuples = new_polymer_tuples

    char_count = Counter()
    for (first, last), count in polymer_tuples.items():
        char_count[first] += count
        char_count[last] += count

    char_count[polymer[0]] += 1
    char_count[polymer[-1]] += 1

    sorted_map = char_count.most_common()
    print(sorted_map[0][1]//2 - sorted_map[-1][1]//2)


if __name__ == '__main__':
    main()