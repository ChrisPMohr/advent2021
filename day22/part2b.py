from collections import defaultdict, Counter


def get_range(coords):
    a1, a2 = coords.split("=")[1].split("..")
    return int(a1), int(a2) + 1


def do_intersect(ranges1, ranges2):
    def _do_intersect(ranges1, ranges2):
        return all(ranges1[i][1] < ranges2[i][0] for i in range(3))

    return _do_intersect(ranges1, ranges2) or _do_intersect(ranges2, ranges1)


def segment_range(existing_range, new_range):
    if not do_intersect(existing_range, new_range):
        return [existing_range]


def main():
    lines = open('example.txt', 'r').readlines()
    # lines = open('input.txt', 'r').readlines()

    lines.reverse()

    all_xs = set()
    all_ys = set()
    all_zs = set()
    ranges = []

    num_pixels = 0
    for line in lines:
        print(line.strip())
        command, coords = line.strip().split(" ")
        xs, ys, zs = coords.split(",")
        xs = get_range(xs)
        ys = get_range(ys)
        zs = get_range(zs)

        if command == 'on':
            num_pixels += (xs[1] - xs[0]) * (ys[1] - ys[0]) * (zs[1] - zs[0])

    print(num_pixels)


if __name__ == '__main__':
    main()
