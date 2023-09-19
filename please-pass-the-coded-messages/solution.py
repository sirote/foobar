"""
Please Pass the Coded Messages
==============================
You need to pass a message to the bunny workers, but to avoid detection, the
code you agreed to use is... obscure, to say the least. The bunnies are given
food on standard-issue plates that are stamped with the numbers 0-9 for easier
sorting, and you need to combine sets of plates to create the numbers in the
code. The signal that a number is part of the code is that it is divisible by
3. You can do smaller numbers like 15 and 45 easily, but bigger numbers like
144 and 414 are a little trickier. Write a program to help yourself quickly
create large numbers for use in the code, given a limited number of plates to
work with.

You have L, a list containing some digits (0 to 9). Write a function
solution(L) which finds the largest number that can be made from some or all of
these digits and is divisible by 3. If it is not possible to make such a
number, return 0 as the solution. L will contain anywhere from 1 to 9 digits.
The same digit may appear multiple times in the list, but each element in the
list may only be used once.
"""

from itertools import permutations


def solution(digits):
    """Find the largest number divisible by 3."""
    for candidate in iter_candidates(digits):
        if candidate % 3 == 0:
            return candidate

    return 0


def iter_candidates(digits):
    """Generate all possible candidates from highest to lowest."""
    sorted_digits = sorted(digits, reverse=True)
    for size in range(len(sorted_digits), 0, -1):
        seen = set()
        for candidate in permutations(sorted_digits, r=size):
            if candidate not in seen:
                seen.add(candidate)
                yield to_number(candidate)


def to_number(digits):
    """Convert a list of digits to a number."""
    return sum(d * 10**i for i, d in enumerate(reversed(digits)))


if __name__ == '__main__':
    assert solution([3, 1, 4, 1]) == 4311
    assert solution([3, 1, 4, 1, 5, 9]) == 94311
