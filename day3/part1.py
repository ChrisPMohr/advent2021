def main():
    lines = open('input.txt', 'r').readlines()
    nums = []
    num_lines = len(lines)
    num_size = len(lines[0])
    digit_counter = [0 for _ in range(num_size - 1)]
    for line in lines:
        for i, digit in enumerate(line):
            if digit == '1':
                digit_counter[i] += 1

    gamma_num = []
    for counter in digit_counter:
        if counter >= num_lines / 2:
            gamma_num.append('1')
        else:
            gamma_num.append('0')

    gamma_num = int(''.join(gamma_num), 2)
    ep_num = (2 ** (num_size -1)) - 1 - gamma_num
    print(gamma_num * ep_num)


if __name__ == '__main__':
    main()