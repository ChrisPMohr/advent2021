from collections import defaultdict, Counter


def main():
    # text = open('example.txt', 'r').readline().strip()
    text = open('input.txt', 'r').readline().strip()
    _, _, x, y = text.split(" ")
    _, x_vals = x.strip(",").split("=")
    _, y_vals = y.split("=")
    x_min, x_max = map(int, x_vals.split(".."))
    y_min, y_max = map(int, y_vals.split(".."))
    print(x_min, x_max, y_min, y_max)

    max_y_pos = -1000

    for init_y_vel in range(1, 1000):
        for init_x_vel in range(1, 1000):
            iter_max_y = -1000
            # print("vel = ", init_x_vel, init_y_vel)
            x_vel = init_x_vel
            y_vel = init_y_vel
            found_sol = False
            pos = (0, 0)
            while pos[0] <= x_max and pos[1] >= y_min:
                pos = (pos[0] + x_vel, pos[1] + y_vel)
                # print("new_pos = ", pos)
                if pos[1] > iter_max_y:
                    iter_max_y = pos[1]
                if x_vel > 0:
                    x_vel -= 1
                elif x_vel < 0:
                    x_vel += 1
                y_vel -= 1
                if x_min <= pos[0] <= x_max and y_min <= pos[1] <= y_max:
                    found_sol = True
                    print(init_x_vel, init_y_vel)
                    break
            if found_sol:
                max_y_pos = iter_max_y
    print(max_y_pos)


if __name__ == '__main__':
    main()