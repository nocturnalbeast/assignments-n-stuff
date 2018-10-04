from collections import Counter

ONES = 1
TWOS = 2
THREES = 3
FOURS = 4
FIVES = 5
SIXES = 6
FULL_HOUSE = 7
FOUR_OF_A_KIND = 8
LITTLE_STRAIGHT = 9
BIG_STRAIGHT = 10
CHOICE = 11
YACHT = 12

def score(dice, category):
    if category < 7:
    	return dice.count(category) * category
    elif category == FULL_HOUSE:
    	return int(sorted(Counter(dice).values()) == [2,3]) * sum(dice)
    elif category == FOUR_OF_A_KIND:
    	try:
    		count = Counter(dice)
    		return 4 * (int(5 in count.values()) | int(4 in count.values())) * count.most_common(1)[0][0]
    	except ValueError as e:
    		return 0
    elif category == LITTLE_STRAIGHT:
    	return int(sorted(dice) == [1,2,3,4,5]) * 30
    elif category == BIG_STRAIGHT:
    	return int(sorted(dice) == [2,3,4,5,6]) * 30
    elif category == CHOICE:
    	return sum(dice)
    elif category == YACHT:
        return int(dice[0] == dice[1] == dice[2] == dice[3] == dice[4]) * 50