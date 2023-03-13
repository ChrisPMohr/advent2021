from collections import defaultdict, Counter


def get_range(coords):
    return tuple(map(int, coords.split("=")[1].split("..")))


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()


    on_cubes = set()
    for line in lines:
        command, coords = line.strip().split(" ")
        xs, ys, zs = coords.split(",")
        xs = get_range(xs)
        ys = get_range(ys)
        zs = get_range(zs)
        for x in range(max(-50, xs[0]), min(51, xs[1]+1)):
            for y in range(max(-50, ys[0]), min(51, ys[1] + 1)):
                for z in range(max(-50, zs[0]), min(51, zs[1] + 1)):
                    if command == 'on':
                        on_cubes.add((x,y,z))
                    else:
                        if (x,y,z) in on_cubes:
                            on_cubes.remove((x,y,z))
    print(len(on_cubes))


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