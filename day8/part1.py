from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    inputs = []
    for line in lines:
        num_segments, input_nums = line.strip().split(" | ")
        print(num_segments, input_nums)
        inputs.append((num_segments.split(" "), input_nums.split(" ")))

    print(inputs[0])

    print(sum(1 for num in inputs[0][1] if len(num) in {2, 3, 4, 7}))
    print(
        sum(sum(1 for num in input[1] if len(num) in {2,3,4,7}) for input in inputs)
    )

if __name__ == '__main__':
    main()