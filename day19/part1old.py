from collections import defaultdict, Counter


def compute_axis(diff1, diff2):
    axis = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            if abs(diff2[i]) == abs(diff1[j]):
                if diff2[i] == diff1[j]:
                    axis[i] = j + 1
                else:
                    axis[i] = -(j + 1)
    return axis


def coord_diff(first, second):
    return tuple(first[i] - second[i] for i in range(3))


def get_beacon_and_diff(scanner1, scanner2, normalized_scanner1, normalized_scanner2):
    overlapping_diffs = list(
        set(normalized_scanner1.keys()).intersection(set(normalized_scanner2.keys())))
    diff1 = overlapping_diffs[2]
    scanner1_beacon1, scanner1_beacon2 = normalized_scanner1[diff1]
    scanner2_beacon1, scanner2_beacon2 = normalized_scanner2[diff1]

    scanner1_beacon = scanner1_beacon1
    for diff2 in overlapping_diffs:
        scanner1_beacon3, scanner1_beacon4 = normalized_scanner1[diff2]
        if diff2 != diff1 and (scanner1_beacon3 == scanner1_beacon1 or scanner1_beacon4 == scanner1_beacon1):
            scanner2_beacon3, scanner2_beacon4 = normalized_scanner2[diff2]
            if scanner2_beacon1 == scanner2_beacon3 or scanner2_beacon1 == scanner2_beacon4:
                print("scanner2_beacon1 is scanner1_beacon1")
                scanner2_beacon = scanner2_beacon1
                break
            elif scanner2_beacon2 == scanner2_beacon3 or scanner2_beacon2 == scanner2_beacon4:
                print("scanner2_beacon1 is scanner1_beacon1")
                scanner2_beacon = scanner2_beacon2
                break
            else:
                print("Problem!")

    diff1 = coord_diff(scanner1[scanner1_beacon2], scanner1[scanner1_beacon1])
    diff2 = coord_diff(scanner2[scanner2_beacon2], scanner2[scanner2_beacon1])

    return scanner1[scanner1_beacon], scanner2[scanner2_beacon], diff1, diff2


def invert_axis(axis):
    inverted_axis = [0, 0, 0]
    for i in range(3):
        inverted_axis[abs(axis[i]) - 1] = axis[i] // abs(axis[i]) * (i + 1)
    return inverted_axis


def get_nums_from_tuples(tuples):
    s = set()
    for t in tuples:
        for v in t:
            s.add(v)
    return s


def main():
    lines = open('example.txt', 'r').readlines()
    # lines = open('input.txt', 'r').readlines()

    scanners = [list()]
    scanner_num = 0

    for line in lines:
        line = line.strip()
        if line.startswith("--- "):
            continue
        if not line:
            scanner_num += 1
            scanners.append(list())
            continue
        coords = tuple(map(int, line.split(",")))
        scanners[-1].append(coords)

    scanners_diff = [dict()]
    for scanner in scanners:
        for i in range(len(scanner)-1):
            for j in range(i + 1, len(scanner)):
                diff_x = scanner[i][0] - scanner[j][0]
                diff_y = scanner[i][1] - scanner[j][1]
                diff_z = scanner[i][2] - scanner[j][2]
                scanners_diff[-1][(diff_x, diff_y, diff_z)] = (i, j)
        scanners_diff.append(dict())
    scanners_diff.pop()

    # Figure out which beacons are the same as one another
    normalized_scanners = []
    for scanner_diff in scanners_diff:
        normalized_scanners.append({tuple(sorted(map(abs, coords))): beacons for coords, beacons in scanner_diff.items()})

    overlapping_scanners = []
    overlapping_scanner_edges = defaultdict(list)

    for i in range(len(normalized_scanners) - 1):
        for j in range(i + 1, len(normalized_scanners)):
            scanner1 = normalized_scanners[i]
            scanner2 = normalized_scanners[j]
            overlapping_diffs = set(scanner1.keys()).intersection(set(scanner2.keys()))
            if len(get_nums_from_tuples(scanner1[diff] for diff in overlapping_diffs)) >= 12:
                overlapping_scanners.append((i, j))
                overlapping_scanner_edges[i].append(j)
    # print(overlapping_scanners)

    # tuple ((x, y, z), (axis 1, axis 2, axis 3))
    scanner_offsets = {}
    total_offsets = {0: ((0,0,0), (1,2,3))}

    for i, j in overlapping_scanners:
        normalized_scanner1 = normalized_scanners[i]
        normalized_scanner2 = normalized_scanners[j]
        scanner1 = scanners[i]
        scanner2 = scanners[j]

        beacon_coords1, beacon_coords2, diff1, diff2 = get_beacon_and_diff(
            scanner1, scanner2, normalized_scanner1, normalized_scanner2)

        axis = compute_axis(diff1, diff2)

        offset = tuple(beacon_coords2[a] - axis[a]//abs(axis[a]) * beacon_coords1[abs(axis[a])-1] for a in range(3))
        scanner_offsets[(i, j)] = (offset, axis)
        inverted_axis = invert_axis(axis)
        rev_offset = tuple(beacon_coords1[a] - inverted_axis[a]//abs(inverted_axis[a]) * beacon_coords2[abs(inverted_axis[a])-1] for a in range(3))
        scanner_offsets[(j, i)] = (rev_offset, inverted_axis)
        if i == 0:
            total_offsets[j] = (offset, axis)

    print(scanner_offsets)

    # scanner_offset, axis = total_offsets[1]
    # for beacon in scanners[1]:
    #     print(tuple(scanner_offset[a] + axis[a]//abs(axis[a]) * beacon[abs(axis[a])-1] for a in range(3)))

    offset_queue = list(overlapping_scanner_edges[0])
    while offset_queue and len(total_offsets) < len(scanners):
        print("-" * 40)
        print("total_offsets", total_offsets)
        next_beacon = offset_queue.pop(0)
        print("working from beacon", next_beacon)
        for i in range(len(scanners)):
            if i in total_offsets:
                continue
            if (next_beacon, i) in scanner_offsets:
                print("-" * 20)
                print("from beacon", next_beacon, "connecting to", i)
                offset1, axis1 = total_offsets[next_beacon]
                offset2, axis2 = scanner_offsets[(next_beacon, i)]
                print("absolute offset from 0", total_offsets[next_beacon])
                print("relative offset", scanner_offsets[(next_beacon, i)])
                new_offset = tuple(offset1[a] + axis1[a]//abs(axis1[a]) * offset2[abs(axis1[a])-1] for a in range(3))
                new_axis = tuple(axis1[a]//abs(axis1[a]) * axis2[abs(axis1[a])-1] for a in range(3))
                total_offsets[i] = (new_offset, new_axis)
                offset_queue.append(i)
                print("new absolute offset from 0", new_offset, new_axis)



    print("total_offsets", total_offsets)


    # find map of overlapping sets

    # can this include relative positions + orientations?

    # if so, then can just follow the graph from scanner 0 to find all scanners + orientations

    # then find position of all beacons relative to scanner 0




if __name__ == '__main__':
    main()