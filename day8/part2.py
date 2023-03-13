from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    inputs = []
    total = 0
    for line in lines:
        num_segments, input_nums = line.strip().split(" | ")
        num_segments = [''.join(sorted(s)) for s in num_segments.split(" ")]
        input_nums = [''.join(sorted(s)) for s in input_nums.split(" ")]
        inputs.append((num_segments, input_nums))

        decoded_map = {}
        rev_map = {}
        six_patterns = []
        five_patterns = []
        for input_num in num_segments:
            if len(input_num) == 2:
                decoded_map[input_num] = 1
                rev_map[1] = input_num
            if len(input_num) == 3:
                decoded_map[input_num] = 7
                rev_map[7] = input_num
            if len(input_num) == 4:
                decoded_map[input_num] = 4
                rev_map[4] = input_num
            if len(input_num) == 5:
                five_patterns.append(input_num)
            if len(input_num) == 6:
                six_patterns.append(input_num)
            if len(input_num) == 7:
                decoded_map[input_num] = 8
                rev_map[8] = input_num

        for pattern in six_patterns:
            if set(rev_map[7]) - set(pattern):
                decoded_map[pattern] = 6
                rev_map[6] = pattern
                break
        six_patterns.remove(rev_map[6])

        for pattern in five_patterns:
            if len(set(rev_map[1]).intersection(set(pattern))) == 2:
                decoded_map[pattern] = 3
                rev_map[3] = pattern
                break
        five_patterns.remove(rev_map[3])

        for pattern in six_patterns:
            if len(set(pattern).intersection(set(rev_map[3]))) == 5:
                decoded_map[pattern] = 9
                rev_map[9] = pattern
                break
        six_patterns.remove(rev_map[9])
        decoded_map[six_patterns[0]] = 0
        rev_map[0] = six_patterns[0]

        for pattern in five_patterns:
            if len(set(rev_map[9]).intersection(set(pattern))) == 5:
                decoded_map[pattern] = 5
                rev_map[5] = pattern
                break
        five_patterns.remove(rev_map[5])
        decoded_map[five_patterns[0]] = 2
        rev_map[2] = five_patterns[0]

        total_input_value = 0
        for value in input_nums:
            total_input_value *= 10
            total_input_value += decoded_map[value]
        print(total_input_value)

        total += total_input_value

    print(total)


if __name__ == '__main__':
    main()