from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    algo = [1 if c == '#' else 0 for c in lines[0].strip()]


    image = defaultdict(int)
    for y, line in enumerate(lines[2:]):
        for x, c in enumerate(line.strip()):
            if c == '#':
                image[(x, y)] = 1

    min_x = -30
    min_y = -30
    orig_max_x = len(lines[2].strip()) + 3
    orig_max_y = len(lines[2:]) + 3
    max_x = len(lines[2].strip()) + 30
    max_y = len(lines[2:]) + 30

    print(image)

    for _ in range(2):
        new_image = defaultdict(int)
        for i in range(min_x, max_x+1):
            for j in range(min_y, max_y+1):
                pixels = []
                for dj in range(-1, 2):
                    for di in range(-1, 2):
                        pixels.append(image[(i + di, j + dj)])
                algo_index = int(''.join(str(i) for i in pixels), 2)
                new_image[(i,j)] = algo[algo_index]
                print(i, j, new_image[(i, j)], algo_index)
        max_y += 30
        max_x += 30
        min_x -= 30
        min_y -= 30
        image = new_image
        for j in range(min_y, max_y+1):
            print("".join('#' if image[(i,j)] else '.' for i in range(min_x, max_x+1)))

        print(sum(
            v for (i,j), v in image.items() if -5 < i < orig_max_x + 4 and -5 < j < orig_max_y))










if __name__ == '__main__':
    main()