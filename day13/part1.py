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
            print(axis, num)
            if axis == "y":
                for x, y in dots:
                    if y < num:
                        new_dots.add((x,y))
                    if y > num:
                        new_dots.add((x, num - (y - num)))
                dots = new_dots
                break
            else:
                for x, y in dots:
                    if x < num:
                        new_dots.add((x,y))
                    if x > num:
                        new_dots.add((num - (x - num), y))
                dots = new_dots
                break

    print(sum(1 for v in dots))




    # items = {}
    # for y, line in enumerate(lines):
    #     for x, c in enumerate(line.strip()):
    #         items[(x, y)] = int(c)


if __name__ == '__main__':
    main()