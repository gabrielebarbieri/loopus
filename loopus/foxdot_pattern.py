from abc import ABC, abstractmethod
from itertools import cycle


def xtraverse(pattern):

    if isinstance(pattern, tuple):
        for child in pattern:
            for element in xtraverse(child):
                yield element
    elif isinstance(pattern, cycle):
        child = next(pattern)
        for element in xtraverse(child):
            yield element
    else:
        yield pattern


def parse(pattern):
    if isinstance(pattern, list):
        return cycle(parse(e) for e in pattern)
    elif isinstance(pattern, tuple):
        return tuple(parse(e) for e in pattern)
    else:
        return pattern


def recursive_cycle(pattern):
    parsed_pattern = parse(pattern)
    while True:
        for e in xtraverse(parsed_pattern):
            yield e


class AbstractPattern(ABC):

    def __add__(self, other):
        if not isinstance(other, AbstractPattern):
            other = Pattern(other)
        return PatternOperation(self, other, lambda x, y: x+y)

    @abstractmethod
    def __next__(self):
        pass

    def __radd__(self, other):
        return self + other


class Pattern(AbstractPattern):

    def __init__(self, *pattern):
        self.pattern = pattern
        self.cycle = recursive_cycle(self.pattern)

    def __next__(self):
        return next(self.cycle)

    def clone(self):
        return Pattern(self.pattern)

    def __repr__(self):
        if len(self.pattern) == 1:
            return f'P({self.pattern[0]})'
        return f'P{self.pattern}'


class PatternOperation(AbstractPattern):

    def __init__(self, p1, p2, operation):
        self.p1 = p1
        self.p2 = p2
        self.operation = operation

    def __next__(self):
        return self.operation(next(self.p1), next(self.p2))

    def __repr__(self):
        return f'{self.p1} + {self.p2}'


P = Pattern
