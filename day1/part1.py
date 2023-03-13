def main():
    input_text = open('input.txt', 'r').readlines()
    input_vals = [int(line) for line in input_text]
    pairs = zip(input_vals[:-1], input_vals[1:])
    print(sum(1 for x, y in pairs if x < y))


if __name__ == '__main__':
    main()