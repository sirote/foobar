"""Braille Translation
===================
Because Commander Lambda is an equal-opportunity despot, they have several
visually-impaired minions. But Lambda never bothered to follow intergalactic
standards for workplace accommodations, so those minions have a hard time
navigating her space station. You figure printing out Braille signs will help
them, and -- since you'll be promoting efficiency at the same time -- increase
your chances of a promotion.

Braille is a writing system used to read by touch instead of by sight. Each
character is composed of 6 dots in a 2x3 grid, where each dot can either be a
bump or be flat (no bump). You plan to translate the signs around the space
station to Braille so that the minions under Commander Lambda's command can
feel the bumps on the signs and "read" the text with their touch. The special
printer which can print the bumps onto the signs expects the dots in the
following order:
1 4
2 5
3 6

So given the plain text word "code", you get the Braille dots:

11 10 11 10
00 01 01 01
00 10 00 00

where 1 represents a bump and 0 represents no bump. Put together, "code"
becomes the output string "100100101010100110100010".

Write a function solution(plaintext) that takes a string parameter and returns
a string of 1's and 0's representing the bumps and absence of bumps in the
input string. Your function should be able to encode the 26 lowercase letters,
handle capital letters by adding a Braille capitalization mark before that
character, and use a blank character (000000) for spaces. All signs on the
space station are less than fifty characters long and use only letters and
spaces.
"""


def solution(string):
    """Encode a string into Braille."""
    pangram = 'The quick brown fox jumps over the lazy dog'
    braille = (
        '000001011110110010100010'
        '000000111110101001010100'
        '100100101000000000110000'
        '111010101010010111101110'
        '000000110100101010101101'
        '000000010110101001101100'
        '111100011100000000101010'
        '111001100010111010000000'
        '011110110010100010000000'
        '111000100000101011101111'
        '000000100110101010110110'
    )
    return Translator(pangram, braille).encode(string)


class Translator:
    """A translator from a string to Braille."""

    def __init__(self, pangram, braille):
        self._pangram = pangram
        self._braille = braille
        self._cap_mark = object()
        self._table = self._make_table()

    @property
    def table(self):
        """A table of Braille codes for each character."""
        return self._table

    def encode(self, string):
        """Encode a string into Braille."""
        return ''.join(self._encode(string))

    def _encode(self, string):
        for char in string:
            if char.isupper():
                yield self.table[self._cap_mark]
                yield self.table[char.lower()]
            else:
                yield self.table[char]

    def _make_table(self):
        """Create a table of Braille codes for each character in the
        pangram.
        """
        table = {}
        codes = _chunk(self._braille, 6)
        for char in self._pangram:
            if char.isupper():
                table[self._cap_mark] = next(codes)
                table[char.lower()] = next(codes)
            else:
                table[char] = next(codes)

        return table


def _chunk(string, size):
    for i in range(0, len(string), size):
        yield string[i:i + size]
