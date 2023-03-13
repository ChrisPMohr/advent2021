from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    dots = set()
    is_dots = True
    for line in lines:
        line = line.strip()
        if not line:
            is_dots = False
            continue

        if is_dots:
            x, y = line.split(",")
            dots.add((int(x), int(y)))
        else:
            _, _, instruction = line.split(" ")
            axis, num = instruction.split("=")
            num = int(num)

            new_dots = set()
            if axis == "y":
                for x, y in dots:
                    if y < num:
                        new_dots.add((x,y))
                    if y > num:
                        new_dots.add((x, num - (y - num)))
                dots = new_dots
            else:
                for x, y in dots:
                    if x < num:
                        new_dots.add((x,y))
                    if x > num:
                        new_dots.add((num - (x - num), y))
                dots = new_dots

    max_x = max(x for x,y in dots)
    max_y = max(y for x,y in dots)
    for y in range(0, max_y + 1):
        print("".join('#' if (x,y) in dots else ' ' for x in range(0, max_x+10)))


if __name__ == '__main__':
    main()