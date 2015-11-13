__author__ = 'jessem'

import random

def roll_less_lowest(dice_sides, dice_no, remove):
    rolls = []
    for i in range(dice_no):
        rolls.append(random.randint(1,dice_sides))

    rolls.remove(min(rolls))

    return sum(rolls)

def main():
    test_results = []

    for i in range(10000):
        test_results.append(roll_less_lowest(6, 4, 1))

    results = sum(test_results) / len(test_results)

    print(results)


if __name__ == '__main__':
    main()