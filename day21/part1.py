from collections import defaultdict, Counter
from itertools import cycle


def main():
    lines = open('example.txt', 'r').readlines()
    # lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    dice = cycle(range(1, 101))

    p1 = 5
    p2 = 10

    p1_points = 0
    p2_points = 0

    rolls = 0

    while p2_points <= 1000:
        roll = next(dice) + next(dice) + next(dice)
        rolls += 3
        p1 = (p1 + roll - 1) % 10 + 1
        p1_points += p1

        if p1_points >= 1000:
            break

        roll = next(dice) + next(dice) + next(dice)
        rolls += 3
        p2 = (p2 + roll - 1) % 10 + 1
        p2_points += p2

    print(p1, p1_points, p2, p2_points, rolls)





if __name__ == '__main__':
    main()