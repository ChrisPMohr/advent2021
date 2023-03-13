from collections import defaultdict, Counter


def fun(n):
    return n * (n+1) / 2

def main():
    nums = list(map(int, open('input.txt', 'r').readline().split(',')))
    print(nums)

    max_num = max(nums)

    max_val = 100000000**2
    for i in range(max_num):
        max_val = min(sum(fun(abs(num - i)) for num in nums), max_val)
    print(max_val)



if __name__ == '__main__':
    main()