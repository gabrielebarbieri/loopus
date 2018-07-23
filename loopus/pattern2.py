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
        yield next(pattern)
    else:
        yield pattern


def recursive_cycle(pattern):
    while True:
        for e in visitor(pattern):
            yield e

if __name__ == '__main__':
    o = cycle([3, 4])
    p = [0, [cycle([1, o]), 7, 8, 9]]
    c = recursive_cycle(p)
    for _ in xrange(100):
        print next(c)