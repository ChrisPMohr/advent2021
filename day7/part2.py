def fun(n):
    return n * (n+1) / 2


def main():
    nums = list(map(int, open('input.txt', 'r').readline().split(',')))
    min_value = 100000000**2
    for i in range(max(nums)):
        min_value = min(sum(fun(abs(num - i)) for num in nums), min_value)

    print(min_value)


if __name__ == '__main__':
    main()