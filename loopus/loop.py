from loopus.pattern import Pattern
from loopus.clock import clock


class Loop(object):

    compensation = 0.1

    def __init__(self, durations, actions, *params):
        self.durations = Pattern(durations)
        self.actions = Pattern(actions)
        self.parameters = [Pattern(p) for p in params]
        self.running = False
        self.play()

    def play(self):
        self.running = True
        beat = clock.next_bar
        print(beat)
        self.loop(beat)

    def stop(self):
        self.running = False

    def loop(self, beat):
        if self.running:
            dur = next(self.durations)
            action = next(self.actions)
            params = [next(p) for p in self.parameters]
            clock.schedule(beat, action, *params)
            next_beat = beat + dur
            clock.schedule(next_beat - self.compensation, self.loop, next_beat)


if __name__ == '__main__':
    l = Loop([1, 0.5], print, ['hello', 'bonjour'], 'world')
