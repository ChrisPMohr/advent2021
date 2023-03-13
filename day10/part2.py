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

    error_scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    auto_scores = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }

    scores = []

    for line in lines:
        open_chunks = []
        error = False
        for char in line.strip():
            if char in {'{', '[', '<', '('}:
                open_chunks.append(char)
            else:
                if open_chunks[-1] == matching_chunk[char]:
                    open_chunks.pop()
                else:
                    # total_score += error_scores[char]
                    error = True
                    break

        if not error and open_chunks:
            print(open_chunks)
            score = 0
            for char in reversed(open_chunks):
                score *= 5
                score += auto_scores[char]
            scores.append(score)

    print(scores)

    print(sorted(scores)[(len(scores) - 1)//2])



if __name__ == '__main__':
    main()