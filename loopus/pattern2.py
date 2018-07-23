from itertools import cycle


# class Or(object):
#
#     def __init__(self, seq):
#         self.cycle = cycle(seq)
#
#     def next(self):
#         return next(self.cycle)


def visitor(pattern):

    if isinstance(pattern, list):
        for child in pattern:
            for element in visitor(child):
                yield element
    elif isinstance(pattern, cycle):
        child = next(pattern)
        for element in visitor(child):
            yield element
    else:
        yield pattern


def recursive_cycle(pattern):
    while True:
        for e in visitor(pattern):
            yield e

if __name__ == '__main__':
    o = cycle([1, 2])
    p = cycle([0, o, [3, 4]])
    c = recursive_cycle(p)
    for _ in xrange(10):
        print next(c)