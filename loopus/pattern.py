def recursive_cycle(iterable):
    """
    recursive cycle in case of nested list:
    [A, B] -> A B A B ...
    [A, [1, 2]] -> A 1 A 2 A 1 A 2 ...
    [(1, 2), A] -> (1, 2) A (1, 2) A ...
    :param iterable:
    :return:
    """
    saved = []
    for element in iterable:
        if isinstance(element, list):
            p = recursive_cycle(element)
            yield next(p)
            saved.append(p)
        else:
            yield element
            saved.append(element)

    while saved:
        for element in saved:
            try:
                yield next(element)
            except TypeError:
                yield element


class AbstractPattern(object):

    def __add__(self, other):
        if not isinstance(other, AbstractPattern):
            other = Pattern(other)
        return PatternOperation(self, other, lambda x, y: x+y)

    def __radd__(self, other):
        return self + other


class Pattern(AbstractPattern):

    def __init__(self, pattern):
        self.pattern = pattern if isinstance(pattern, list) else [pattern]
        self.cycle = recursive_cycle(self.pattern)

    def __next__(self):
        return next(self.cycle)

    def clone(self):
        return Pattern(self.pattern)

    def __repr__(self):
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


class PatternFactory(object):

    def __getitem__(self, item):
        if isinstance(item, tuple):
            item = list(item)
        return Pattern(item)


P = PatternFactory()
