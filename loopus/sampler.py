from loopus.player import Player
from music21.pitch import Pitch


def get_mapping(samples, starting_point):
    if isinstance(starting_point, str):
        starting_point = Pitch(starting_point).midi
    mapping = {s: i+starting_point for i, s in enumerate(samples)}
    mapping[' '] = 0
    return mapping


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
    return tuple(result)


def compute_durations(sequence, step_duration=None):
    if step_duration is None:
        step_duration = len(sequence) / 2

    if isinstance(sequence, list):
        return [compute_durations(e, step_duration) for e in sequence]
    if isinstance(sequence, tuple):
        return tuple(compute_durations(e, step_duration / len(sequence)) for e in sequence)
    return step_duration


class Sampler(Player):

    def __init__(self, clock, mapping, sequence, sus=None, channel=0):
        samples = parse(sequence)
        dur = compute_durations(samples)
        super(Sampler, self).__init__(clock, mapping, samples, dur, sus, channel)

    def get_pitch(self, degree):
        return self.scale[degree]


if __name__ == '__main__':
    mapping = get_mapping('xrocOX-T.t=Ww*C+', 'C2')
    from loopus.clock import Clock
    from time import sleep
    c = Clock()

    c.start()
    s = Sampler(c, mapping, 'x(=-)(*c)[( X)(---)]', channel=1)
    s.play()
    sleep(10)
    s.stop()
    sleep(1)
    c.stop()
