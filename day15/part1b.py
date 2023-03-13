from collections import defaultdict, Counter

def est_cost(coord, destination):
    return 1*(destination[0] - coord[0] + destination[1] - coord[1])


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    destination = (len(lines[0])-2, len(lines)-1)
    risks = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            risks[(x, y)] = int(c)

    direction = [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]

    lowest_risk = {}


    items = defaultdict(list)
    items[est_cost((0,0), destination)].append(((0,0), 0))
    min_length = None
    while items:
        min_estimated_risk = min(items.keys())
        coord, risk = items[min_estimated_risk].pop()
        if not items[min_estimated_risk]:
            del items[min_estimated_risk]
        if coord in lowest_risk and risk > lowest_risk[coord]:
            continue
        lowest_risk[coord] = risk
        if coord == destination:
            if min_length is None or risk < min_length:
                min_length = risk
                print(min_length)
        for dir in direction:
            new_coord = (coord[0] + dir[0], coord[1] + dir[1])
            if new_coord not in risks:
                continue
            new_risk = risk + risks[new_coord]
            estimated_risk = est_cost(new_coord, destination) + new_risk
            items[estimated_risk].append((new_coord, new_risk))

    print(min_length)

    # max_x = max(x for x,y in items)
    # max_y = max(y for x,y in items)
    # for y in range(0, max_y + 1):
    #     print("".join('#' if (x,y) in items else ' ' for x in range(0, max_x+10)))


if __name__ == '__main__':
    main()