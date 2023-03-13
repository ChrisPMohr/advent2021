import bisect
from itertools import product


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
    lines = open('input.txt', 'r').readlines()

    lines.reverse()

    all_xs = set()
    sorted_xs = []
    all_ys = set()
    sorted_ys = []
    all_zs = set()
    sorted_zs = []
    ranges = []

    intersecting_ranges = set()

    num_pixels = 0
    for line in lines:
        command, coords = line.strip().split(" ")
        xs, ys, zs = coords.split(",")
        xs = get_range(xs)
        ys = get_range(ys)
        zs = get_range(zs)

        # Update sorted list of subranges
        if xs[0] not in all_xs:
            all_xs.add(xs[0])
            bisect.insort(sorted_xs, xs[0])
        if xs[1] not in all_xs:
            all_xs.add(xs[1])
            bisect.insort(sorted_xs, xs[1])
        if ys[0] not in all_ys:
            all_ys.add(ys[0])
            bisect.insort(sorted_ys, ys[0])
        if ys[1] not in all_ys:
            all_ys.add(ys[1])
            bisect.insort(sorted_ys, ys[1])
        if zs[0] not in all_zs:
            all_zs.add(zs[0])
            bisect.insort(sorted_zs, zs[0])
        if zs[1] not in all_zs:
            all_zs.add(zs[1])
            bisect.insort(sorted_zs, zs[1])

        if command == 'on':
            in_range_xs = []
            in_range_ys = []
            in_range_zs = []
            for x1, x2 in zip(sorted_xs[:-1], sorted_xs[1:]):
                if x1 >= xs[0] and x2 <= xs[1]:
                    in_range_xs.append((x1, x2))
            for y1, y2 in zip(sorted_ys[:-1], sorted_ys[1:]):
                if y1 >= ys[0] and y2 <= ys[1]:
                    in_range_ys.append((y1, y2))
            for z1, z2 in zip(sorted_zs[:-1], sorted_zs[1:]):
                if z1 >= zs[0] and z2 <= zs[1]:
                    in_range_zs.append((z1, z2))

            in_ranges = set(product(*[in_range_xs, in_range_ys, in_range_zs])) - intersecting_ranges

            for (x1, x2), (y1, y2), (z1, z2) in in_ranges:
                did_intersect = False
                for (a1, a2), (b1, b2), (c1, c2) in ranges:
                    if (a1 <= x1 <= x2 <= a2) and (b1 <= y1 <= y2 <= b2) and (c1 <= z1 <= z2 <= c2):
                        did_intersect = True
                        break
                if not did_intersect:
                    new_pixels = (x2 - x1) * (y2 - y1) * (z2 - z1)
                    num_pixels += new_pixels
                else:
                    intersecting_ranges.add((x1, x2, y1, y2, z1, z2))

        ranges.append((xs, ys, zs))

    print(num_pixels)


if __name__ == '__main__':
    main()
