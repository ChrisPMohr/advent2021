from collections import defaultdict, Counter
import itertools
import numpy as np
from numpy.linalg import inv


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
    # for from_scanner_rotation, from_scanner_beacons in from_scanner_rotations:
    from_scanner_rotation, from_scanner_beacons = from_scanner_rotations[0]

    for to_scanner_rotation, to_scanner_beacons in to_scanner_rotations:
        displacements = Counter(
            tuple(from_beacon - to_beacon) for from_beacon, to_beacon
            in itertools.product(from_scanner_beacons, to_scanner_beacons))
        # displacements = Counter()
        # for from_scanner_beacon in from_scanner_beacons:
        #     for to_scanner_beacon in to_scanner_beacons:
        #         displacement = tuple(from_scanner_beacon - to_scanner_beacon)
        #         displacements.update({displacement: 1})
        most_common_displacement, count = displacements.most_common(1)[0]
        if count >= 12:
            # print("Found common reference frame", np.matmul(from_scanner_rotation, -np.array(most_common_displacement))) #, from_scanner_rotation, to_scanner_rotation)
            # for from_beacon in from_scanner_beacons:
            #     for to_beacon in to_scanner_beacons:
            #         displacement = tuple(from_beacon - to_beacon)
            #         if displacement == most_common_displacement:
            #             print(
            #                 np.matmul(from_scanner_rotation, from_beacon),
            #                 np.matmul(inv(to_scanner_rotation).astype(int), to_beacon),
            #                 np.matmul(inv(to_scanner_rotation).astype(int), np.matmul(from_scanner_rotation, from_beacon) - np.array(displacement))
            #             )
            return np.array(most_common_displacement), from_scanner_rotation, to_scanner_rotation
    return None, None, None


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # lines = open('example1.txt', 'r').readlines()

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
    # print(len(all_rots))
    # print(all_rots[:6])

    all_beacon_rotations = [generate_beacon_rotations(beacons, all_rots) for beacons in scanners]
    print("Generated all rotated beacon lists")
    # for scanner_beacon_rotations in all_beacon_rotations:
    #     for beacon_rotation in scanner_beacon_rotations:
    #         print(beacon_rotation)

    # find_matching_rotations(all_beacon_rotations[0], all_beacon_rotations[1])
    overlapping_scanners = {}
    scanner_to_scanner = defaultdict(set)
    for scanner1 in range(len(scanners)):
        for scanner2 in range(len(scanners)):
            if scanner1 == scanner2:
                continue
        # for scanner2 in range(scanner1 + 1, len(scanners)):
            print("Searching for match between", scanner1, scanner2)
            displacement, scanner1_rotation, scanner2_rotation = find_matching_rotations(
                all_beacon_rotations[scanner1], all_beacon_rotations[scanner2])
            if displacement is not None:
                overlapping_scanners[(scanner1, scanner2)] = (
                    displacement,
                    scanner1_rotation,
                    inv(scanner2_rotation).astype(int))
                # overlapping_scanners[(scanner2, scanner1)] = (
                #     -displacement,
                #     inv(scanner2_rotation).astype(int),
                #     inv(scanner1_rotation).astype(int))
                # print(overlapping_scanners[(scanner2, scanner1)])
                scanner_to_scanner[scanner1].add(scanner2)
                # scanner_to_scanner[scanner2].add(scanner1)
        # print(f"Found all scanners overlapping with scanner {scanner1}")

    print("Found all overlapping scanners")
    # print(overlapping_scanners.keys())

    # included_scanners = {0, 11}
    # included_scanners = {0, 1, 4}
    # included_scanners = {0, 1, 2, 3, 4}
    # included_scanners = {0, 1, 3, 4}
    included_scanners = {0}

    for start_scanner in included_scanners:
        all_beacons = set()
        processed_scanners = set()
        scanners_to_process = [(start_scanner, [])]
        while scanners_to_process:
            scanner, chain = scanners_to_process.pop(0)
            if scanner in processed_scanners:
                continue
            # if scanner not in included_scanners:
            #     continue
            processed_scanners.add(scanner)
            print("processing", scanner, chain)
            scanner_beacons = scanners[scanner].copy()
            for from_scanner, to_scanner in chain:
                print(f"Doing chain {from_scanner} -> {to_scanner}")
                displacement, rot_from, rot_to = overlapping_scanners[(from_scanner, to_scanner)]
                print(displacement)
                print(rot_from)
                print(rot_to)
                for i in range(len(scanner_beacons)):
                    b = scanner_beacons[i]
                    scanner_beacons[i] = np.matmul(rot_to, np.matmul(rot_from, scanner_beacons[i]) - displacement)
                    print(f"{b} -> {scanner_beacons[i]}")
            # print(scanner, set(map(tuple, scanner_beacons)))
            all_beacons.update(set(map(tuple, scanner_beacons)))
            # for beacon in scanner_beacons:
            #     beacon_tuple = tuple(beacon)
            #     if beacon_tuple not in all_beacons:
            #         print("Adding", beacon)
            #         all_beacons.add(beacon_tuple)

            for next_scanner in scanner_to_scanner[scanner]:
                scanners_to_process.append((next_scanner, [(next_scanner, scanner)] + chain))

        # print(all_beacons)
        print(f"From {start_scanner}, can see {len(all_beacons)} different beacons")
        print("-" * 40)
        print("\n".join([str(b) for b in sorted(list(all_beacons))]))






if __name__ == '__main__':
    main()