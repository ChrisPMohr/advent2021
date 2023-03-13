def main():
    lines = open('input.txt', 'r').readlines()

    line_segments = []
    max_x = 0
    max_y = 0
    for line in lines:
        coord1, coord2 = line.strip().split(' -> ')
        x1, y1 = coord1.split(',')
        x2, y2 = coord2.split(',')
        line_segments.append((int(x1),int(y1),int(x2),int(y2)))
        max_x = max(max_x, int(x1), int(x2))
        max_y = max(max_y, int(y1), int(y2))

    coords = {}
    for x in range(0, max_x+1):
        for y in range(0, max_y+1):
            coords[(x,y)] = 0

    for line_segment in line_segments:
        x1, y1, x2, y2 = line_segment
        if x1 == x2:
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            for y in range(min_y, max_y+1):
                coords[(x1, y)] += 1
        elif y1 == y2:
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            for x in range(min_x, max_x+1):
                coords[(x, y1)] += 1

    count = 0
    for val in coords.values():
        if val > 1:
            count += 1

    print(count)


if __name__ == '__main__':
    main()