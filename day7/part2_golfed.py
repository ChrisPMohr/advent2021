def fun(n):
    return n * (n+1) / 2


def main():
    nums = list(map(int, open('input.txt', 'r').readline().split(',')))
    print(min(sum(fun(abs(num - i)) for num in nums) for i in range(max(nums))))


if __name__ == '__main__':
    main()