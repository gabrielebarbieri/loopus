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
        if not isinstance(pattern, list):
            pattern = [pattern]
        self.pattern = recursive_cycle(pattern)

    # def __iter__(self):
    #     return self

    def __next__(self):
        return next(self.pattern)


if __name__ == '__main__':
    p = Pattern([1, 2, 2])
    for _ in range(10):
        print(next(p))
