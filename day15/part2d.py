from collections import defaultdict, Counter
from heapq import heappush, heappop, nsmallest


def est_cost(coord, destination):
    return 1*(destination[0] - coord[0] + destination[1] - coord[1])


def main():
    lines = open('example.txt', 'r').readlines()
    # lines = open('input.txt', 'r').readlines()

    destination = (len(lines[0])-2, len(lines)-1)
    risks = {}
    unvisited = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            for i in range(0,5):
                for j in range(0,5):
                    end_x = x + i * (destination[0] + 1)
                    end_y = y + j * (destination[1] + 1)
                    end_risk = (int(c) + i + j - 1) % 9 + 1
                    risks[(end_x, end_y)] = end_risk
                    unvisited.add((end_x, end_y))
    destination = (5*(len(lines[0])-1) - 1, 5*(len(lines))- 1)

    direction = [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]

    distances = {(0, 0): 0}
    distance_q = [(0, (0,0))]

    while distance_q:
        dist, coord = heappop(distance_q)
        if coord not in unvisited:
            continue
        unvisited.remove(coord)
        if coord == destination:
            print(dist)
            break
        for dir in direction:
            new_coord = (coord[0] + dir[0], coord[1] + dir[1])
            if new_coord not in risks:
                continue
            new_dist = dist + risks[new_coord]
            if new_coord not in distances or new_dist < distances[new_coord]:
                distances[new_coord] = new_dist
                heappush(distance_q, (new_dist, new_coord))


if __name__ == '__main__':
    main()