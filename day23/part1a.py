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
room_depth = 2

letter_points = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

map_positions = {}
for x in range(13):
    map_positions[(x, -1)] = "#"
map_positions[(0, 0)] = "#"
map_positions[(12, 0)] = "#"
map_positions[(0, 1)] = "#"
map_positions[(1, 1)] = "#"
map_positions[(11, 1)] = "#"
map_positions[(12, 1)] = "#"
for x in range(2, 11):
    map_positions[(x, 3)] = "#"
for x in range(2, 12, 2):
    map_positions[(x, 1)] = "#"
    map_positions[(x, 2)] = "#"


def print_positions(positions, depth, total_cost):
    grid_positions = dict(map_positions)
    for c in "ABCD":
        for pos in positions[c]:
            grid_positions[pos] = c

    print("-" * 13)
    print(positions)
    print(f"Depth: {depth} - Cost: {sum(total_cost)}, {total_cost}")
    for y in range(-1, 4):
        for x in range(13):
            print(grid_positions.get((x, y), " "), end="")
        print("")
    print("-" * 13)


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


count = 0


def get_available_moves(positions):
    global count
    count += 1
    moves = []

    occupied_holding_spot = set()
    room_movables = list()
    room_occupants = {x: [] for x in allowed_occupants.keys()}
    room_all_allowed = set()
    for letter, poses in positions.items():
        # print(letter, poses)
        for x, y in poses:
            if y == 0:
                occupied_holding_spot.add((x, letter))
            if y > 0:
                room_occupants[x].append((y, letter))

    for x, this_room_occupants in room_occupants.items():
        if this_room_occupants:
            y, letter = sorted(this_room_occupants)[0]
            room_movables.append(((x, y), letter))
        allowed_occupant = allowed_occupants[x]
        if all(letter == allowed_occupant for _, letter in this_room_occupants):
            room_all_allowed.add(x)

    # print("occupied holding spots", sorted(list(occupied_holding_spot)))
    # print("room movables", sorted(list(room_movables)))
    # print("room occupants", sorted(room_occupants.items()))
    # print("Room only allowed occupants", room_all_allowed)

    for x, letter in occupied_holding_spot:
        y = 0
        end_x = final_columns[letter]

        if end_x < x and any(end_x < i < x for i, _ in occupied_holding_spot):
            continue
        if end_x > x and any(end_x > i > x for i, _ in occupied_holding_spot):
            continue
        this_room_occupants = room_occupants[end_x]
        if end_x in room_all_allowed:
            # move to final column if accessible
            moves.append((letter, (x, y), (end_x, room_depth - len(this_room_occupants))))

    for (x, y), letter in room_movables:
        if x == final_columns[letter] and x in room_all_allowed:
            continue
        smaller_holding_spots = [i for i in holding_spots if i < x]
        larger_holding_spots = [i for i in holding_spots if i > x]
        for i in smaller_holding_spots:
            if not any(i <= j < x for j, _ in occupied_holding_spot):
                moves.append((letter, (x, y), (i, 0)))
        for i in larger_holding_spots:
            if not any(i >= j > x for j, _ in occupied_holding_spot):
                moves.append((letter, (x, y), (i, 0)))
    # print("available moves", moves)
    return moves


memoizer = {}

required_moves = {}
# required_moves = {
#     0: ("B", (7, 1), (4, 0)),
#     1: ("C", (5, 1), (6, 0)),
#     2: ("C", (6, 0), (7, 1)),
#     3: ("D", (5, 2), (6, 0)),
#     4: ("B", (4, 0), (5, 2))
# }

min_total_points = 1000000


def dfs(positions, depth=0, total_cost=[]):
    global min_total_points

    if depth > 20:
    # if depth > 6:
        return None
    position_tuple = tuple((k, tuple(v)) for k, v in positions.items())
    if position_tuple in memoizer:
        if memoizer[position_tuple][1] <= sum(total_cost):
            return None

    if num_valid_room_occupants(positions) == 8:
        return 0

    # approximate remaining cost
    approximate_remaining_cost = 0
    for letter, col in final_columns.items():
        for x, y in positions[letter]:
            if x != col:
                num_moves = abs(x - col) + y + 1
                approximate_remaining_cost += num_moves * letter_points[letter]
    if approximate_remaining_cost + sum(total_cost) > min_total_points:
        return None

    # print_positions(positions, depth, total_cost)
    available_moves = get_available_moves(positions)

    min_points = None
    for letter, start, end in available_moves:
        if depth in required_moves:
            if required_moves[depth] != (letter, start, end):
                continue
        # print(f"Doing {letter} {start}->{end}")
        move_points = score_move(letter, start, end)
        new_position = deepcopy(positions)
        new_position[letter].remove(start)
        new_position[letter].append(end)
        new_position_point = dfs(new_position, depth+1, total_cost+[move_points])
        if new_position_point is None:
            continue
        new_points = new_position_point + move_points
        if min_points is None or new_points < min_points:
            min_points = new_points
        if new_points + sum(total_cost) < min_total_points:
            min_total_points = new_points + sum(total_cost)

    memoizer[position_tuple] = (min_points, sum(total_cost))
    # if min_points is None:
    #     print("No moves available from")
    #     print_positions(positions, depth)
    return min_points


def main():
    # lines = open('example.txt', 'r').readlines()
    lines = open('input.txt', 'r').readlines()

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

    print(dfs(positions))
    print(count)

if __name__ == '__main__':
    main()