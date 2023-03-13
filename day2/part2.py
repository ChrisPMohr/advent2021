def main():
    lines = open('input.txt', 'r').readlines()
    horiz = 0
    aim = 0
    vert = 0
    for line in lines:
        command, dist = line.split()
        dist = int(dist)
        if command == 'forward':
            horiz += dist
            vert += dist * aim
        elif command == 'down':
            aim += dist
        elif command == 'up':
            aim -= dist
    print(horiz*vert)


if __name__ == '__main__':
    main()