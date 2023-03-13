from collections import defaultdict, Counter


class Snailfish(object):
    def __init__(self, left, right):
        self.left = left
        if isinstance(left, Snailfish):
            left.parent = self
        self.right = right
        if isinstance(right, Snailfish):
            right.parent = self
        self.parent = None

    def __repr__(self):
        return '[' + str(self.left) + ',' + str(self.right) + ']'


def parse_num(s):
    # print('parsing', s)
    s = s[1:-1]
    if s[0] == '[':
        counter = 0
        offset = None
        for i in range(len(s)):
            if s[i] == '[':
                counter += 1
            if s[i] == ']':
                counter -= 1
            # print(s[i], counter)
            if counter == 0:
                offset = i
                break
        # print("Found left", s[0:offset+1], "right", s[offset+2:])
        left = parse_num(s[0:offset+1])
        if s[offset+2] == '[':
            right = parse_num(s[offset+2:])
        else:
            right = int(s[offset+2:])
    else:
        left_s, right_s = s.split(",", 1)
        # print(left_s, right_s)
        left = int(left_s)
        if right_s[0] == '[':
            right = parse_num(right_s)
        else:
            right = int(right_s)
    return Snailfish(left, right)


def find_deep_num(num, i=0):
    if isinstance(num, int):
        return None
    if i == 4:
        return num
    if i < 4:
        if isinstance(num.left, Snailfish):
            deep_num = find_deep_num(num.left, i+1)
            if deep_num:
                return deep_num
        if isinstance(num.right, Snailfish):
            deep_num = find_deep_num(num.right, i+1)
            if deep_num:
                return deep_num


def find_big_num(num, i=0):
    if isinstance(num.left, Snailfish):
        big_num = find_big_num(num.left, i + 1)
        if big_num:
            return big_num
    else:
        if num.left >= 10:
            return num
    if isinstance(num.right, Snailfish):
        big_num = find_big_num(num.right, i + 1)
        if big_num:
            return big_num
    else:
        if num.right >= 10:
            return num
    return None


def explode_num(num):
    parent = num.parent
    if num == parent.right:
        if isinstance(parent.left, Snailfish):
            child = parent.left
            while isinstance(child.right, Snailfish):
                child = child.right
            child.right += num.left
        else:
            parent.left += num.left
        # parent.left += num.left

        # add to right

        # go up until this is on the left branch
        # go down the right child's left branch

        sub_parent = num
        super_parent = parent
        while super_parent.parent:
            super_parent = super_parent.parent
            sub_parent = sub_parent.parent

            if super_parent.left == sub_parent:
                # print("sub", sub_parent)
                # print("super", super_parent)
                if isinstance(super_parent.right, Snailfish):
                    child = super_parent.right
                    while isinstance(child.left, Snailfish):
                        child = child.left
                    # print("child", child)
                    child.left += num.right
                else:
                    super_parent.right += num.right
                break

        parent.right = 0
    else:
        # add to right
        if isinstance(parent.right, Snailfish):
            child = parent.right
            while isinstance(child.left, Snailfish):
                child = child.left
            child.left += num.right
        else:
            parent.right += num.right
        parent.left = 0

        # add to left

        # go up until this is on the right branch
        # go down the left child's right branch


        sub_parent = num
        super_parent = parent
        while super_parent.parent:
            super_parent = super_parent.parent
            sub_parent = sub_parent.parent

            if super_parent.right == sub_parent:
                # print("sub", sub_parent)
                # print("super", super_parent)
                if isinstance(super_parent.left, Snailfish):
                    child = super_parent.left
                    while isinstance(child.right, Snailfish):
                        child = child.right
                    # print("child", child)
                    child.right += num.left
                else:
                    super_parent.left += num.left
                break

def split_num(num):
    if isinstance(num.left, int) and num.left >= 10:
        n = num.left
        new_num = Snailfish(n//2, n - n//2)
        new_num.parent = num
        num.left = new_num
    else:
        n = num.right
        new_num = Snailfish(n//2, n - n//2)
        new_num.parent = num
        num.right = new_num


def process_num(num):
    has_action = True
    while has_action:
        # print(num)
        deep_num = find_deep_num(num)
        if deep_num:
            # print("Found deep num", deep_num)
            explode_num(deep_num)
        else:
            big_num = find_big_num(num)
            if big_num:
                # print("Found big num", big_num)
                split_num(big_num)
            else:
                has_action = False


def add_nums(num1, num2):
    new_num = Snailfish(num1, num2)
    process_num(new_num)
    return new_num


def magnitude(num):
    left = num.left
    right = num.right
    if isinstance(left, Snailfish):
        mag_left = magnitude(left)
    else:
        mag_left = left
    if isinstance(right, Snailfish):
        mag_right = magnitude(right)
    else:
        mag_right = right
    return 3*mag_left + 2*mag_right



def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()
    # nums = list(map(int, open('example.txt', 'r').readline().split(',')))
    # nums = list(map(int, open('input.txt', 'r').readline().split(',')))

    nums = []
    for line in lines[0:]:
        nums.append(parse_num(line.strip()))

    best_magnitude = 0
    for i in range(0, len(lines)-1):
        for j in range(i, len(lines)):
            num1 = parse_num(lines[i].strip())
            num2 = parse_num(lines[j].strip())
            m1 = magnitude(add_nums(num1, num2))
            num1 = parse_num(lines[i].strip())
            num2 = parse_num(lines[j].strip())
            m2 = magnitude(add_nums(num2, num1))
            best_magnitude = max(best_magnitude, m1, m2)
    print(best_magnitude)

    # items = {}
    # for y, line in enumerate(lines):
    #     for x, c in enumerate(line.strip()):
    #         items[(x, y)] = int(c)

    # max_x = max(x for x,y in items)
    # max_y = max(y for x,y in items)
    # for y in range(0, max_y + 1):
    #     print("".join('#' if (x,y) in items else ' ' for x in range(0, max_x+10)))


if __name__ == '__main__':
    main()