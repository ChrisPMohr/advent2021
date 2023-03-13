from collections import defaultdict, Counter


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

    matching_chunk = {
        '}': '{',
        '>': '<',
        ']': '[',
        ')': '('
    }

    score = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    total_score = 0

    for line in lines:
        open_chunks = []
        for char in line.strip():
            if char in {'{', '[', '<', '('}:
                open_chunks.append(char)
            else:
                if open_chunks[-1] == matching_chunk[char]:
                    open_chunks.pop()
                else:
                    total_score += score[char]
                    break

    print(total_score)



if __name__ == '__main__':
    main()