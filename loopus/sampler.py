def get_mapping(samples, starting_point):
    return {s: i+starting_point for i, s in enumerate(samples)}


def parse(sequence):
    result = []
    stack = [result]
    for s in sequence:
        if s == '[' or s == '(':
            stack.append([])
        elif s == ']':
            e = stack.pop()
            if len(e) == 1:
                e = e[0]
            stack[-1].append(e)
        elif s == ')':
            e = stack.pop()
            if len(e) == 1:
                stack[-1].append(e[0])
            else:
                stack[-1].append(tuple(e))
        else:
            stack[-1].append(s)
    return result


print(parse('X-[s(tu)z]-'))
