"""
Doomsday Fuel
=============
Making fuel for the LAMBCHOP's reactor core is a tricky process because of the
exotic matter involved. It starts as raw ore, then during processing, begins
randomly changing between forms, eventually reaching a stable form. There may
be multiple stable forms that a sample could ultimately reach, not all of which
are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation
efficiency by predicting the end state of a given ore sample. You have
carefully studied the different structures that the ore can take and which
transitions it undergoes. It appears that, while random, the probability of
each structure transforming is fixed. That is, each time the ore is in 1 state,
it has the same probabilities of entering the next state (which might be the
same state). You have recorded the observed transitions in a matrix. The others
in the lab have hypothesized more exotic forms that the ore can become, but you
haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints
representing how many times that state has gone to the next state and return an
array of ints for each terminal state giving the exact probabilities of each
terminal state, represented as the numerator for each state, then the
denominator for all of them at the end and in simplest form. The matrix is at
most 10 by 10. It is guaranteed that no matter which state the ore is in, there
is a path from that state to a terminal state. That is, the processing will
always eventually end in a stable state. The ore starts in state 0. The
denominator will fit within a signed 32-bit integer during the calculation, as
long as the fraction is simplified regularly.

For example, consider the matrix m:
[
[0,1,0,0,0,1], # s0, the initial state, goes to s1 and s5 with equal
                 probability
[4,0,0,3,2,0], # s1 can become s0, s3, or s4, but with different probabilities
[0,0,0,0,0,0], # s2 is terminal, and unreachable (never observed in practice)
[0,0,0,0,0,0], # s3 is terminal
[0,0,0,0,0,0], # s4 is terminal
[0,0,0,0,0,0], # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in
the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
"""


from copy import deepcopy
from fractions import Fraction
from functools import reduce
from math import gcd


def solution(matrix):
    """Return the probabilities of each terminal state."""
    if sum(matrix[0]) == 0:
        return [1, *(0 for row in matrix[1:] if sum(row) == 0), 1]

    transition_matrix = normalize(matrix)
    q_matrix, r_matrix = canonical_form(transition_matrix)
    identity = IdentityMatrix(q_matrix.shape[0])
    n_matrix = (identity - q_matrix) ** -1
    b_matrix = n_matrix * r_matrix
    probabilities = b_matrix[0]
    denominator = lcm(fraction.denominator for fraction in probabilities)
    return [*(
        int(probability * denominator)
        for probability in probabilities
    ), denominator]


def normalize(matrix):
    """Convert a matrix to a transition matrix."""
    transition_matrix = []
    for row in matrix:
        denominator = sum(row)
        if denominator == 0:
            fractions = [Fraction(0, 1) for _ in row]
        else:
            fractions = [
                Fraction(numerator, denominator)
                for numerator in row
            ]

        transition_matrix.append(fractions)

    return transition_matrix


def canonical_form(matrix):
    """Convert a transition matrix to canonical form."""
    transients = []
    absorbings = []

    for state, row in enumerate(matrix):
        if all(v == 0 for v in row):
            absorbings.append(state)
        else:
            transients.append(state)

    q_matrix = [
        [matrix[state][j] for j in transients]
        for state in transients
    ]
    r_matrix = [
        [matrix[state][j] for j in absorbings]
        for state in transients
    ]

    return Matrix(q_matrix), Matrix(r_matrix)


class Matrix:
    """A matrix."""

    def __init__(self, matrix):
        self.matrix = matrix

    def __getitem__(self, key):
        return self.matrix[key]

    def __add__(self, other):
        """Add two matrices."""
        return Matrix([
            [
                self.matrix[i][j] + other.matrix[i][j]
                for j in range(len(self.matrix[i]))
            ]
            for i in range(len(self.matrix))
        ])

    def __sub__(self, other):
        """Subtract two matrices."""
        return Matrix([
            [
                self.matrix[i][j] - other.matrix[i][j]
                for j in range(len(self.matrix[i]))
            ]
            for i in range(len(self.matrix))
        ])

    def __mul__(self, other):
        """Multiply two matrices or a matrix with scalar."""
        if isinstance(other, (int, Fraction)):
            return Matrix([
                [
                    self.matrix[i][j] * other
                    for j in range(len(self.matrix[i]))
                ]
                for i in range(len(self.matrix))
            ])

        if isinstance(other, Matrix):
            return Matrix([
                [
                    sum(
                        self.matrix[i][k] * other.matrix[k][j]
                        for k in range(len(self.matrix[i]))
                    )
                    for j in range(len(other.matrix[0]))
                ]
                for i in range(len(self.matrix))
            ])

        raise NotImplementedError

    def __pow__(self, power):
        """Raise a matrix to a power."""
        if power == 0:
            return IdentityMatrix(self.shape[0])

        if power == 1:
            return Matrix(deepcopy(self.matrix))

        if power == -1:
            return self.inverse()

        raise NotImplementedError

    @property
    def shape(self):
        """Return the shape of the matrix."""
        return len(self.matrix), len(self.matrix[0])

    @property
    def determinant(self):
        """Return the determinant of the matrix."""
        if self.shape == (1, 1):
            return self.matrix[0][0]

        if self.shape == (2, 2):
            return (
                self.matrix[0][0] * self.matrix[1][1]
                - self.matrix[0][1] * self.matrix[1][0]
            )

        return sum(
            (-1)**i * self.matrix[0][i] * self.minor(0, i).determinant
            for i in range(self.shape[0])
        )

    def transpose(self):
        """Return the transpose of the matrix."""
        return Matrix([
            [
                self.matrix[j][i]
                for j in range(self.shape[0])
            ]
            for i in range(self.shape[1])
        ])

    def minor(self, i, j):
        """Return the minor matrix of the element."""
        return Matrix([
            [
                self.matrix[x][y]
                for y in range(self.shape[1])
                if y != j
            ]
            for x in range(self.shape[0])
            if x != i
        ])

    def cofactor(self):
        """Return the cofactor of the matrix."""
        return Matrix([
            [
                (-1)**(i + j) * self.minor(i, j).determinant
                for j in range(self.shape[1])
            ]
            for i in range(self.shape[0])
        ])

    def adjoint(self):
        """Return the adjoint of the matrix."""
        return self.cofactor().transpose()

    def inverse(self):
        """Return the inverse of the matrix."""
        determinant = self.determinant
        if self.shape == (1, 1):
            return Matrix([
                [Fraction(1, determinant)]
            ])

        if self.shape == (2, 2):
            return Matrix([
                [self.matrix[1][1], -self.matrix[0][1]],
                [-self.matrix[1][0], self.matrix[0][0]],
            ]) * Fraction(1, determinant)

        return self.adjoint() * Fraction(1, determinant)


class IdentityMatrix(Matrix):
    """An identity matrix."""

    def __init__(self, size):
        super().__init__([
            [
                1 if i == j else 0
                for j in range(size)
            ]
            for i in range(size)
        ])


def lcm(numbers):
    """Return the least common multiple of numbers."""
    return reduce(lambda x, y: (x * y) // gcd(x, y), numbers, 1)


if __name__ == '__main__':
    assert solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]) == [7, 6, 8, 21]
    assert solution([
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]) == [0, 3, 2, 9, 14]
    assert solution([
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ]) == [1, 0, 1]
