dice_distribution = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

def main():
    p1 = 5
    p2 = 10

    distribution = {
        (p1, 0, p2, 0): 1
    }

    total_points = 21

    while True:
        # roll dice for p1
        new_distribution = defaultdict(int)
        for key, pos_weight in distribution.items():
            pos, points, p2_pos, p2_points = key
            if max(points, p2_points) < total_points:
                for roll, count in dice_distribution.items():
                    new_pos = (pos + roll - 1) % 10 + 1
                    new_points = points + new_pos
                    new_distribution[(new_pos, new_points, p2_pos, p2_points)] += pos_weight * count
            else:
                new_distribution[(pos, points, p2_pos, p2_points)] += pos_weight
        distribution = new_distribution

        if all(max(p1_points, p2_points) >= total_points for _, p1_points, _, p2_points in distribution.keys()):
            print("done")
            break

        # roll dice for p2
        new_distribution = defaultdict(int)
        for key, pos_weight in distribution.items():
            p1_pos, p1_points, pos, points = key
            if max(p1_points, points) < total_points:
                for roll, count in dice_distribution.items():
                    new_pos = (pos + roll - 1) % 10 + 1
                    new_points = points + new_pos
                    new_distribution[(p1_pos, p1_points, new_pos, new_points)] += pos_weight * count
            else:
                new_distribution[(p1_pos, p1_points, pos, points)] += pos_weight
        distribution = new_distribution

        if all(max(p1_points, p2_points) >= total_points for _, p1_points, _, p2_points in distribution.keys()):
            print("done")
            break

    print(sum(count for (_, p1_points, _, p2_points), count in distribution.items() if p1_points > p2_points))
    print(sum(count for (_, p1_points, _, p2_points), count in distribution.items() if p1_points < p2_points))


if __name__ == '__main__':
    main()