from collections import defaultdict, Counter


def parse_packet(bits, i):
    version = int(''.join(bits[i: i + 3]), 2)
    print("v", version)
    version_sum = version
    i += 3
    id_type = int(''.join(bits[i: i + 3]), 2)
    print("id", id_type)
    i += 3
    if id_type == 4:
        print("parsing literal value")
        while bits[i] == '1':
            print(bits[i:i+5])
            i += 5
        print(bits[i:i + 5])
        i += 5
    else:
        print("parsing operator packet")
        len_id = bits[i]
        i += 1
        if len_id == '0':
            print(bits[i:i+15])
            length = int(''.join(bits[i:i + 15]), 2)
            i += 15
            total_length = 0
            print("parsing length", length)
            while total_length < length:
                print("parsing subpacket")
                new_i, sub_version_sum = parse_packet(bits, i)
                total_length += (new_i - i)
                i = new_i
                version_sum += sub_version_sum
        else:
            num_subpackets = int(''.join(bits[i:i + 11]), 2)
            i += 11
            print("parsing subpackets", num_subpackets)
            for j in range(num_subpackets):
                print("parsing subpacket")
                new_i, sub_version_sum = parse_packet(bits, i)
                i = new_i
                version_sum += sub_version_sum
    return i, version_sum

def main():
    # bits = list(bin(int(open('example.txt', 'r').readline(), 16))[2:])
    bits = list(bin(int(open('input.txt', 'r').readline(), 16))[2:])

    while len(bits) % 4 != 0:
        bits.insert(0, '0')

    print(bits)

    i = 0
    total_version_sum = 0
    while i + 8 < len(bits):
        i, version_sum = parse_packet(bits, i)
        total_version_sum += version_sum

    print("total version", total_version_sum)


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