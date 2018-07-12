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


class Pattern(object):

    def __init__(self, pattern):
        self.pattern = pattern if isinstance(pattern, list) else [pattern]
        self.cycle = recursive_cycle(self.pattern)

    # def __iter__(self):
    #     return self

    def __next__(self):
        return next(self.cycle)

    def clone(self):
        return Pattern(self.pattern)
