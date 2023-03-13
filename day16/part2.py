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
        literal_value_bits = []
        print("parsing literal value")
        while bits[i] == '1':
            literal_value_bits.extend(bits[i+1:i+5])
            print(bits[i:i+5])
            i += 5
        literal_value_bits.extend(bits[i + 1:i + 5])
        print(bits[i:i + 5])
        i += 5
        literal_value = int(''.join(literal_value_bits), 2)
        print('literal value', literal_value)
        value = literal_value
    else:
        print("parsing operator packet")
        len_id = bits[i]
        i += 1
        values = []
        if len_id == '0':
            print(bits[i:i+15])
            length = int(''.join(bits[i:i + 15]), 2)
            i += 15
            total_length = 0
            print("parsing length", length)
            while total_length < length:
                print("parsing subpacket")
                value, new_i, sub_version_sum = parse_packet(bits, i)
                values.append(value)
                total_length += (new_i - i)
                i = new_i
                version_sum += sub_version_sum
        else:
            num_subpackets = int(''.join(bits[i:i + 11]), 2)
            i += 11
            print("parsing subpackets", num_subpackets)
            for j in range(num_subpackets):
                print("parsing subpacket")
                value, new_i, sub_version_sum = parse_packet(bits, i)
                print("subpacket had value", value)
                values.append(value)
                i = new_i
                version_sum += sub_version_sum
        print("type_id", id_type, "values", values)
        if id_type == 0:
            value = sum(values)
        elif id_type == 1:
            value = 1
            for v in values:
                value *= v
        elif id_type == 2:
            value = min(values)
        elif id_type == 3:
            value = max(values)
        elif id_type == 5:
            value = 1 if values[0] > values[1] else 0
        elif id_type == 6:
            value = 1 if values[0] < values[1] else 0
        elif id_type == 7:
            value = 1 if values[0] == values[1] else 0

    return value, i, version_sum

def main():
    # bits = list(bin(int(open('example.txt', 'r').readline(), 16))[2:])
    bits = list(bin(int(open('input.txt', 'r').readline(), 16))[2:])

    while len(bits) % 4 != 0:
        bits.insert(0, '0')

    print(bits)

    i = 0
    while i + 8 < len(bits):
        value, i, version_sum = parse_packet(bits, i)
        print("Final value", value)


if __name__ == '__main__':
    main()