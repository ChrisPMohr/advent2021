from collections import defaultdict

def main():
    lines = open('input.txt', 'r').readlines()

    line_segments = []
    max_x = 0
    max_y = 0
    for line in lines:
        coord1, coord2 = line.strip().split(' -> ')
        x1, y1 = map(int, coord1.split(','))
        x2, y2 = map(int, coord2.split(','))
        line_segments.append((x1, y1, x2, y2))
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)

    coords = defaultdict(int)

    for line_segment in line_segments:
        x1, y1, x2, y2 = line_segment
        min_x, max_x = sorted((x1, x2))
        min_y, max_x = sorted((y1, y2))
        if x1 == x2:
            for y in range(min_y, max_y + 1):
                coords[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min_x, max_x + 1):
                coords[(x, y1)] += 1
        elif x1 > x2 == y1 > y2:
            for d in range(0, max_x - min_x + 1):
                coords[(min_x + d, min_y + d)] += 1
        else:
            for d in range(0, max_x - min_x + 1):
                coords[(max_x - d, min_y + d)] += 1

    print(sum(1 for v in coords.values() if v > 1))


if __name__ == '__main__':
    main()