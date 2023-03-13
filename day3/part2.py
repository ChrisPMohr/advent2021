def main():
    lines = open('input.txt', 'r').readlines()

    ox_lines = list(lines)
    for i in range(len(lines[0])):
        ox_lines = filter_most_common_digits(ox_lines, i)
        if len(ox_lines) == 1:
            break

    co2_lines = list(lines)
    for i in range(len(lines[0])):
        co2_lines = filter_least_common_digits(co2_lines, i)
        if len(co2_lines) == 1:
            break

    print(int(ox_lines[0][:-1], 2) * int(co2_lines[0][:-1], 2))


def get_most_common_digits(lines):
    num_lines = len(lines)
    num_size = len(lines[0])
    digit_counter = [0 for _ in range(num_size - 1)]

    for line in lines:
        for i, digit in enumerate(line):
            if digit == '1':
                digit_counter[i] += 1

    most_common_digits = []
    for counter in digit_counter:
        if counter >= num_lines / 2:
            most_common_digits.append('1')
        else:
            most_common_digits.append('0')
    return most_common_digits


def filter_most_common_digits(lines, position):
    most_common_digits = get_most_common_digits(lines)
    target_digit = most_common_digits[position]
    return remove_nonmatching_line(lines, target_digit, position)


def filter_least_common_digits(lines, position):
    most_common_digits = get_most_common_digits(lines)
    target_digit = '1' if most_common_digits[position] == '0' else '0'
    return remove_nonmatching_line(lines, target_digit, position)


def remove_nonmatching_line(lines, target, position):
    return [line for line in lines if line[position] == target]


if __name__ == '__main__':
    main()