from collections import defaultdict, Counter
from heapq import heappush, heappop, nsmallest

def est_cost(coord, destination):
    return 1*(destination[0] - coord[0] + destination[1] - coord[1])


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    destination = (len(lines[0])-2, len(lines)-1)
    risks = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            for i in range(0,5):
                for j in range(0,5):
                    end_x = x + i * (destination[0] + 1)
                    end_y = y + j * (destination[1] + 1)
                    end_risk = (int(c) + i + j - 1) % 9 + 1
                    risks[(end_x, end_y)] = end_risk
    destination = (5*(len(lines[0])-1) - 1, 5*(len(lines))- 1)

    direction = [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]

    lowest_risk = {}

    items = defaultdict(list)
    estimated_cost = est_cost((0,0), destination)
    items[estimated_cost].append(((0,0), 0))
    estimated_risks = []
    heappush(estimated_risks, estimated_cost)
    while items:
        min_estimated_risk = heappop(estimated_risks)
        coord, risk = items[min_estimated_risk].pop()
        # print(min_estimated_risk, coord, risk)
        if not items[min_estimated_risk]:
            del items[min_estimated_risk]

        if coord in lowest_risk and risk > lowest_risk[coord]:
            continue
        lowest_risk[coord] = risk

        if coord == destination:
            print(risk)
            break
        for dir in direction:
            new_coord = (coord[0] + dir[0], coord[1] + dir[1])
            if new_coord not in risks:
                continue
            new_risk = risk + risks[new_coord]
            estimated_risk = est_cost(new_coord, destination) + new_risk
            items[estimated_risk].append((new_coord, new_risk))
            heappush(estimated_risks, estimated_risk)

    # max_x = max(x for x,y in items)
    # max_y = max(y for x,y in items)
    # for y in range(0, max_y + 1):
    #     print("".join('#' if (x,y) in items else ' ' for x in range(0, max_x+10)))


if __name__ == '__main__':
    main()