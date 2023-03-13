from collections import defaultdict, Counter
from copy import deepcopy

final_columns = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

allowed_occupants = {
    3: 'A',
    5: 'B',
    7: 'C',
    9: 'D'
}

holding_spots = [1, 2, 4, 6, 8, 10, 11]


letter_points = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


def num_valid_room_occupants(positions):
    count = 0
    for letter, col in final_columns.items():
        for x, y in positions[letter]:
            if x == col:
                count += 1
    return count


def score_move(letter, start, end):
    start_x, start_y = start
    end_x, end_y = end
    return letter_points[letter] * (abs(start_x - end_x) + abs(start_y - end_y))


def get_available_moves(positions):
    moves = []

    occupied_holding_spot = set()
    movable_rooms1 = set()
    movable_rooms2 = set()
    room_occupants = defaultdict(list)
    for letter, poses in positions.items():
        # print(letter, poses)
        for x, y in poses:
            if y == 0:
                occupied_holding_spot.add(x)
            if y == 1:
                room_occupants[x].append(letter)
                movable_rooms1.add(x)
    for letter, poses in positions.items():
        for x, y in poses:
            if y == 2 and x not in movable_rooms1:
                movable_rooms2.add(x)
                room_occupants[x].append(letter)

    # print("occupied holding spots", occupied_holding_spot)
    # print("movable room1", movable_rooms1)
    # print("movable room2", movable_rooms2)
    # print("room occupants", room_occupants)

    for letter, poses in positions.items():
        for x, y in poses:
            if x != final_columns[letter]:
                if y == 0:
                    end_x = final_columns[letter]
                    this_room_occupants = room_occupants[end_x]
                    if len(this_room_occupants) == 0 or (len(this_room_occupants) == 1 and final_columns[this_room_occupants[0]] == end_x):
                        # move to final column if accessible
                        moves.append((letter, (x, y), (end_x, 2 - len(this_room_occupants))))
                if y == 1 or (y == 2 and x in movable_rooms2):
                    accessible_holding_spots = []
                    smaller_holding_spots = [i for i in holding_spots if i < x]
                    larger_holding_spots = [i for i in holding_spots if i > x]
                    for i in smaller_holding_spots:
                        if not any(i < j < x for j in occupied_holding_spot):
                            accessible_holding_spots.append(i)
                    for i in larger_holding_spots:
                        if not any(i > j > x for j in occupied_holding_spot):
                            accessible_holding_spots.append(i)
                    # move to any accessible holding spot
                    for spot_x in accessible_holding_spots:
                        moves.append((letter, (x, y), (spot_x, 0)))
    return moves



def main():
    lines = open('example.txt', 'r').readlines()
    # lines = open('input.txt', 'r').readlines()

    positions = {
        'A': [],
        'B': [],
        'C': [],
        'D': []
    }

    for i in range(3, 11, 2):
        c = lines[2][i]
        positions[c].append((i, 1))
        c = lines[3][i]
        positions[c].append((i, 2))

    print(positions)

    states = [(positions, 0)]
    while states:
        position, points = states.pop(0)
        available_moves = get_available_moves(position)
        if num_valid_room_occupants(position) == 8:
            print(position, available_moves)
        for letter, start, end in available_moves:
            move_points = score_move(letter, start, end)
            new_position = deepcopy(position)
            new_position[letter].remove(start)
            new_position[letter].append(end)
            states.append((new_position, points + move_points))
        print(len(states))


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