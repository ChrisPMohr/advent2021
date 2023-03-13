from collections import defaultdict


def main():
    lines = open('input.txt', 'r').readlines()

    algo = [1 if c == '#' else 0 for c in lines[0].strip()]

    image = defaultdict(int)
    for y, line in enumerate(lines[2:]):
        for x, c in enumerate(line.strip()):
            if c == '#':
                image[(x, y)] = 1

    orig_max_x = len(lines[2].strip()) - 1
    orig_max_y = len(lines[2:]) - 1
    min_x = -10
    min_y = -10
    max_x = len(lines[2].strip()) + 10
    max_y = len(lines[2:]) + 10

    fill = 1

    for step in range(1, 51):
        new_image = defaultdict(int)
        for i in range(min_x, max_x+1):
            for j in range(min_y, max_y+1):
                pixels = []
                for dj in range(-1, 2):
                    for di in range(-1, 2):
                        pixels.append(image[(i + di, j + dj)])
                algo_index = int(''.join(str(i) for i in pixels), 2)
                new_image[(i,j)] = algo[algo_index]
        image = new_image.copy()
        for (i,j) in new_image.keys():
            if not (-step - 3 <= i <= orig_max_x + 3 + step and -step - 3 <= j <= orig_max_y + 3 + step):
                image[(i,j)] = fill
        fill = 1 - fill
        max_y += 4
        max_x += 4
        min_x -= 4
        min_y -= 4

        print(step)
        print(sum(
            v for (i,j), v in image.items() if -step <= i <= orig_max_x + step and -step <= j <= orig_max_y + step))


if __name__ == '__main__':
    main()