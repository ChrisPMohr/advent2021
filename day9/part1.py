from collections import defaultdict, Counter

def is_lower(coords1, coords2, heightmap):
    return coords2 not in heightmap or heightmap[coords1] < heightmap[coords2]

def is_lowest(coords, heightmap):
    x, y= coords
    return (is_lower(coords, (x-1, y), heightmap) and
            is_lower(coords, (x+1, y), heightmap) and
            is_lower(coords, (x, y-1), heightmap) and
            is_lower(coords, (x, y+1), heightmap))


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    heightmap = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            heightmap[(x,y)] = int(c)

    risk_sum = 0
    for coords, height in heightmap.items():
        if is_lowest(coords, heightmap):
            risk_sum += 1 + height

    print(risk_sum)


if __name__ == '__main__':
    main()