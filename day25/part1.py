from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    horiz_cucs = set()
    vert_cucs = set()

    horiz_max = len(lines[0].strip())
    vert_max = len(lines)

    # items = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == '>':
                horiz_cucs.add((x, y))
            elif c == 'v':
                vert_cucs.add((x, y))

    # print(sorted(list(horiz_cucs)))
    # print(sorted(list(vert_cucs)))

    iteration = 0
    while True:
        iteration += 1

        moving_horiz_cucs = set()
        for pos in horiz_cucs:
            x, y = pos
            new_pos = ((x + 1) % horiz_max, y)
            if new_pos not in horiz_cucs and new_pos not in vert_cucs:
                moving_horiz_cucs.add((pos, new_pos))

        for (old_pos, new_pos) in moving_horiz_cucs:
            horiz_cucs.remove(old_pos)
            horiz_cucs.add(new_pos)

        moving_vert_cucs = set()
        for pos in vert_cucs:
            x, y = pos
            new_pos = (x, (y + 1) % vert_max)
            if new_pos not in horiz_cucs and new_pos not in vert_cucs:
                moving_vert_cucs.add((pos, new_pos))

        for (old_pos, new_pos) in moving_vert_cucs:
            vert_cucs.remove(old_pos)
            vert_cucs.add(new_pos)

        if not moving_horiz_cucs and not moving_vert_cucs:
            break

        # print("-" * 20)
        # print(iteration)
        # for y in range(vert_max):
        #     line = []
        #     for x in range(horiz_max):
        #         if (x, y) in horiz_cucs:
        #             line.append(">")
        #         elif (x, y) in vert_cucs:
        #             line.append("v")
        #         else:
        #             line.append(".")
        #     print(''.join(line))
        #
        # print(sorted(list(horiz_cucs)))
        # print(sorted(list(vert_cucs)))
        # if iteration == 100:
        #     break
    print(iteration)

    # max_x = max(x for x,y in items)
    # max_y = max(y for x,y in items)
    # for y in range(0, max_y + 1):
    #     print("".join('#' if (x,y) in items else ' ' for x in range(0, max_x+10)))


if __name__ == '__main__':
    main()