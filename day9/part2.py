from collections import defaultdict, Counter

def is_lower(coords1, coords2, heightmap):
    return coords2 not in heightmap or heightmap[coords1] < heightmap[coords2]

def is_lowest(coords, heightmap):
    x, y= coords
    return (is_lower(coords, (x-1, y), heightmap) and
            is_lower(coords, (x+1, y), heightmap) and
            is_lower(coords, (x, y-1), heightmap) and
            is_lower(coords, (x, y+1), heightmap))


directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    heightmap = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            heightmap[(x,y)] = int(c)

    rev_flow_directions = defaultdict(list)
    low_points = []

    for coords, height in heightmap.items():
        low_point = True
        if height == 9:
            continue
        for direction in directions:
            coords2 = (coords[0] + direction[0], coords[1] + direction[1])
            if coords2 in heightmap and is_lower(coords2, coords, heightmap):
                low_point = False
                rev_flow_directions[coords2].append(coords)
                break

        if low_point:
            low_points.append(coords)

    #for each low point, assemble basin

    basins = []
    for low_point in low_points:
        basin = set()
        current_nodes = rev_flow_directions[low_point]
        while current_nodes:
            current_node = current_nodes.pop(0)
            if current_node in basin:
                continue
            basin.add(current_node)
            current_nodes.extend(rev_flow_directions[current_node])
        print(low_point, basin)
        basins.append(basin)

    s = sorted((len(basin) + 1 for basin in basins), reverse=True)
    print(s[0]*s[1]*s[2])


if __name__ == '__main__':
    main()