from loopus.pattern import Pattern


class Loop(object):

    compensation = 0.1

    def __init__(self, clock, durations, actions, *params):
        self.durations = Pattern(durations)
        self.actions = Pattern(actions)
        self.parameters = [Pattern(p) for p in params]
        self.running = False
        self.clock = clock

    def play(self):
        self.running = True
        beat = self.clock.next_bar
        self.loop(beat)

    def stop(self):
        self.running = False

    def loop(self, beat):
        if self.running:
            dur = next(self.durations)
            self.schedule_action(beat)
            next_beat = beat + dur
            self.clock.schedule(next_beat - self.compensation, self.loop, next_beat)

    def schedule_action(self, beat):
        action = next(self.actions)
        params = [next(p) for p in self.parameters]
        self.clock.schedule(beat, action, *params)
