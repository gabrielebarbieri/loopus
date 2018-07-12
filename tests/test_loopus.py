import unittest
from loopus.pattern import Pattern


class TestPattern(unittest.TestCase):

    def test_pattern(self):
        p = Pattern([1, 'A'])
        res = [next(p) for _ in range(10)]
        assert res == [1, 'A', 1, 'A', 1, 'A', 1, 'A', 1, 'A']

    def test_interlaced_pattern(self):
        p = Pattern(['A', [1, 2]])
        res = [next(p) for _ in range(10)]
        assert res == ['A', 1, 'A', 2, 'A', 1, 'A', 2, 'A', 1]

    def test_pattern_with_tuples(self):
        p = Pattern([(1, 2), 'A'])
        res = [next(p) for _ in range(10)]
        assert res == [(1, 2), 'A', (1, 2), 'A', (1, 2), 'A', (1, 2), 'A', (1, 2), 'A']

