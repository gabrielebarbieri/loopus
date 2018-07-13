import unittest
from loopus import Pattern, P


class TestPattern(unittest.TestCase):

    def test_pattern(self):
        p = Pattern([1, 'A'])
        res = [next(p) for _ in range(10)]
        assert res == [1, 'A', 1, 'A', 1, 'A', 1, 'A', 1, 'A']
        assert p.__repr__() == "P[1, 'A']"

    def test_interlaced_pattern(self):
        p = Pattern(['A', [1, 2]])
        res = [next(p) for _ in range(10)]
        assert res == ['A', 1, 'A', 2, 'A', 1, 'A', 2, 'A', 1]

    def test_pattern_with_tuples(self):
        p = Pattern([(1, 2), 'A'])
        res = [next(p) for _ in range(10)]
        assert res == [(1, 2), 'A', (1, 2), 'A', (1, 2), 'A', (1, 2), 'A', (1, 2), 'A']

    def test_pattern_short_syntax(self):
        p = P[1, 'A']
        res = [next(p) for _ in range(10)]
        assert res == [1, 'A', 1, 'A', 1, 'A', 1, 'A', 1, 'A']
        assert isinstance(p, Pattern)

    def test_pattern_sum(self):
        p = P[1, 2] + P[1] + P[1, 2, 3]
        assert p.__repr__() == 'P[1, 2] + P[1] + P[1, 2, 3]'
        res = [next(p) for _ in range(10)]
        assert res == [3, 5, 5, 4, 4, 6, 3, 5, 5, 4]

        p = P[1, 2] + 1
        res = [next(p) for _ in range(10)]
        assert res == [2, 3, 2, 3, 2, 3, 2, 3, 2, 3]

        p = P[0, 1] + 1 + 1
        res = [next(p) for _ in range(10)]
        assert res == [2, 3, 2, 3, 2, 3, 2, 3, 2, 3]

        p1 = P[1, 2] + 1
        p2 = 1 + P[1, 2]
        for _ in range(10):
            assert next(p1) == next(p2)

        p1 = P[1] + P[1, 2] + P[1, 2]
        p2 = P[1] + (P[1, 2] + P[1, 2])
        for _ in range(10):
            assert next(p1) == next(p2)
