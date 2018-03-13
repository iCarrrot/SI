from collections import defaultdict
import random
from sys import argv

card_order_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                   "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
rev_c_dict = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
              8: "8", 9: "9", 10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}


def check_straight_flush(hand):
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False


def check_four_of_a_kind(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 4]:
        return True
    return False


def check_full_house(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        return True
    return False


def check_flush(hand):
    suits = [i[1] for i in hand]
    if len(set(suits)) == 1:
        return True
    else:
        return False


def check_straight(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    rank_values = [card_order_dict[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        return True
    else:
        # check straight with low Ace
        if set(values) == set(["A", "2", "3", "4", "5"]):
            return True
        return False


def check_three_of_a_kind(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if set(value_counts.values()) == set([3, 1]):
        return True
    else:
        return False


def check_two_pairs(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 2, 2]:
        return True
    else:
        return False


def check_pair(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if 2 in value_counts.values():
        return True
    else:
        return False


def check_hand(hand):
    if check_straight_flush(hand):
        return 9
    if check_four_of_a_kind(hand):
        return 8
    if check_full_house(hand):
        return 7
    if check_flush(hand):
        return 6
    if check_straight(hand):
        return 5
    if check_three_of_a_kind(hand):
        return 4
    if check_two_pairs(hand):
        return 3
    if check_pair(hand):
        return 2
    return 1


hand_dict = {9: "straight-flush", 8: "four-of-a-kind", 7: "full-house", 6: "flush",
             5: "straight", 4: "three-of-a-kind", 3: "two-pairs", 2: "one-pair", 1: "highest-card"}

# print(check_hand(["2H","2C","4H","5H","6H"]))


def create_set(set_type):
    card_set = []
    if set_type == "B":
        for i in range(2, 11):
            for c in "CDHS":
                card_set += [rev_c_dict[i]+c]
        return card_set
    elif set_type == "F":
        for i in range(11, 15):
            for c in "CDHS":
                card_set += [rev_c_dict[i]+c]
        return card_set


def get_hand(card_set):
    hand = set()
    while len(hand) < 5:
        x = card_set[random.randint(0, len(card_set)-1)]
        hand = hand | {x}
    return hand
# print(check_hand(get_hand(create_set("F"))))


def testuj(rounds, repeats):
    for i in range(rounds):
        res = 0
        for j in range(repeats):
            f = get_hand(create_set("F"))
            b = get_hand(create_set("B"))
            # print(f, check_hand(f), b, check_hand(b))
            res = res + 1 if check_hand(f) \
                >= check_hand(b) else res
            
        print(i, " ", res/repeats)


try:
    testuj(int(argv[1]), int(argv[2]))
except:
    testuj(5,10000)
# print(argv)
