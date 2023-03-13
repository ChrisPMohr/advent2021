from collections import defaultdict, Counter
import itertools
import numpy as np
from numpy.linalg import inv


def mat_dist(v1, v2):
    return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1]) + abs(v1[2] - v2[2])


def cos(half_pis):
    if half_pis % 2 == 1:
        return 0
    elif half_pis % 4 == 0:
        return 1
    else:
        return -1


def sin(half_pis):
    if half_pis % 2 == 0:
        return 0
    elif half_pis % 4 == 1:
        return 1
    else:
        return -1


def generate_rotation_matrices():
    x_rots = []
    y_rots = []
    z_rots = []
    for half_pis in range(4):
        x_rots.append(np.array([
            [1, 0, 0],
            [0, cos(half_pis), -sin(half_pis)],
            [0, sin(half_pis), cos(half_pis)]
        ]))
        y_rots.append(np.array([
            [cos(half_pis), 0, sin(half_pis)],
            [0, 1, 0],
            [-sin(half_pis), 0, cos(half_pis)]
        ]))
        z_rots.append(np.array([
            [cos(half_pis), -sin(half_pis), 0],
            [sin(half_pis), cos(half_pis), 0],
            [0, 0, 1]
        ]))

    all_rots = []
    all_rots_set = set()
    for x, y, z in itertools.product(x_rots, y_rots, z_rots):
        rot = np.matmul(z, np.matmul(y, x))
        hashable_rot = tuple(map(tuple, rot))
        if hashable_rot not in all_rots_set:
            all_rots_set.add(hashable_rot)
            all_rots.append(rot)
    return all_rots


def generate_beacon_rotations(beacon_list, rots):
    rotations = []
    for rot in rots:
        new_beacon_list = []
        for beacon in beacon_list:
            new_beacon_list.append(np.matmul(rot, beacon))
        rotations.append((rot, new_beacon_list))
    return rotations


def find_matching_rotations(from_scanner_rotations, to_scanner_rotations):
    from_scanner_rotation, from_scanner_beacons = from_scanner_rotations[0]

    for to_scanner_rotation, to_scanner_beacons in to_scanner_rotations:
        displacements = Counter(
            tuple(from_beacon - to_beacon) for from_beacon, to_beacon
            in itertools.product(from_scanner_beacons, to_scanner_beacons))
        most_common_displacement, count = displacements.most_common(1)[0]
        if count >= 12:
            return np.array(most_common_displacement), from_scanner_rotation, to_scanner_rotation
    return None, None, None


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    # Read input
    scanners = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        scanner_num = int(line.split(" ")[2])
        i += 1
        beacons = []
        while i < len(lines) and lines[i].strip() != "":
            beacons.append(np.array(list(map(int, lines[i].strip().split(",")))))
            i += 1
        i += 1
        scanners.append(beacons)
    print("Read input")

    all_rots = generate_rotation_matrices()
    print("Generated rotation matrices")

    all_beacon_rotations = [generate_beacon_rotations(beacons, all_rots) for beacons in scanners]
    print("Generated all rotated beacon lists")

    overlapping_scanners = {}
    scanner_to_scanner = defaultdict(set)
    for scanner1 in range(len(scanners)):
        for scanner2 in range(len(scanners)):
            if scanner1 == scanner2:
                continue
            displacement, scanner1_rotation, scanner2_rotation = find_matching_rotations(
                all_beacon_rotations[scanner1], all_beacon_rotations[scanner2])
            if displacement is not None:
                overlapping_scanners[(scanner1, scanner2)] = (
                    displacement,
                    scanner1_rotation,
                    inv(scanner2_rotation).astype(int))
                scanner_to_scanner[scanner1].add(scanner2)

    print("Found all overlapping scanners")

    included_scanners = {0}

    for start_scanner in included_scanners:
        all_scanners = []
        processed_scanners = set()
        scanners_to_process = [(start_scanner, [])]
        while scanners_to_process:
            scanner, chain = scanners_to_process.pop(0)
            if scanner in processed_scanners:
                continue
            # if scanner not in included_scanners:
            #     continue
            processed_scanners.add(scanner)
            # print("processing", scanner, chain)
            scanner_pos = np.array([0, 0, 0])
            for from_scanner, to_scanner in chain:
                # print(f"Doing chain {from_scanner} -> {to_scanner}")
                displacement, rot_from, rot_to = overlapping_scanners[(from_scanner, to_scanner)]
                # print(displacement)
                # print(rot_from)
                # print(rot_to)
                scanner_pos = np.matmul(rot_to, np.matmul(rot_from, scanner_pos) - displacement)
            all_scanners.append(tuple(scanner_pos))

            for next_scanner in scanner_to_scanner[scanner]:
                scanners_to_process.append((next_scanner, [(next_scanner, scanner)] + chain))

        max_dist = 0
        for i in range(len(all_scanners)):
            for j in range(i+1, len(all_scanners)):
                d = mat_dist(all_scanners[i], all_scanners[j])
                if d > max_dist:
                    max_dist = d
        print(max_dist)







if __name__ == '__main__':
    main()