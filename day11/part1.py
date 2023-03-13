from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    octopi = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            octopi[(x,y)] = int(c)

    num_flashes = 0
    steps = 100
    for _ in range(steps):
        print(octopi)

        will_flash = []
        has_flashed = set()
        for key in octopi:
            octopi[key] += 1
            if octopi[key] > 9:
                will_flash.append(key)
                has_flashed.add(key)
                num_flashes += 1

        while will_flash:
            x, y = will_flash.pop(0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 or dy != 0:
                        new_coords = (x + dx, y + dy)
                        if new_coords in octopi:
                            octopi[new_coords] += 1
                            if octopi[new_coords] > 9 and new_coords not in has_flashed:
                                will_flash.append(new_coords)
                                has_flashed.add(new_coords)
                                num_flashes += 1

        for coords in has_flashed:
            octopi[coords] = 0

    print(num_flashes)



if __name__ == '__main__':
    main()