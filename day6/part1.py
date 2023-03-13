from collections import defaultdict

def main():
    nums = map(int, open('input.txt', 'r').readline().split(','))
    counter = defaultdict(int)
    for num in nums:
        counter[num] += 1

    max_day = 80

    for day in range(max_day):
        new_counter = defaultdict(int)
        for i in range(1,9):
            new_counter[i-1] = counter[i]

        new_counter[6] += counter[0]
        new_counter[8] += counter[0]

        counter = new_counter

    print(sum(counter.values()))


if __name__ == '__main__':
    main()