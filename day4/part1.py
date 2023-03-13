def main():
    lines = open('input.txt', 'r').readlines()

    numbers = [int(num) for num in lines[0].split(',')]
    lines = lines[2:]

    card_lines = []
    cards = []

    for line in lines:
        line = line.strip('\n')
        if line:
            card_lines.append(line)
        else:
            new_card = {}
            for y, card_line in zip(range(5), card_lines):
                for x, card_num in zip(range(5), card_line.split()):
                    new_card[(x,y)] = (int(card_num), False)
            cards.append(new_card)
            card_lines = []
    new_card = {}
    for y, card_line in zip(range(5), card_lines):
        for x, card_num in zip(range(5), card_line.split()):
            new_card[(x,y)] = (int(card_num), False)
    cards.append(new_card)

    for num in numbers:
        for card in cards:
            update_card(card, num)
            if check_card(card):
                print("Winner")
                print(num * score_card(card))
                return


def update_card(card, num):
    for x in range(5):
        for y in range(5):
            if card[(x,y)][0] == num:
                card[(x,y)] = (num, True)


def check_card(card):
    for x in range(5):
        if all(card[(x,y)][1] for y in range(5)):
            return True

    for y in range(5):
        if all(card[(x,y)][1] for x in range(5)):
            return True

    # if all(card[(x,x)][1] for x in range(5)):
    #     return True
    #
    # if all(card[(x,4-x)][1] for x in range(5)):
    #     return True

    return False


def score_card(card):
    total = 0
    for x in range(5):
         for y in range(5):
             if card[(x,y)][1] == False:
                 total += card[(x,y)][0]
    return total


if __name__ == '__main__':
    main()