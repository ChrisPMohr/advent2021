def main():
    lines = open('input.txt', 'r').readlines()
    horiz = 0
    vert = 0
    for line in lines:
        command, dist = line.split()
        dist = int(dist)
        if command == 'forward':
            horiz += dist
        elif command == 'down':
            vert += dist
        elif command == 'up':
            vert -= dist
    print(horiz*vert)


if __name__ == '__main__':
    main()