from loopus.loop import Loop
from loopus.pattern import Pattern


class TimeVar(Loop):

    def __init__(self, pattern, durations):
        self.pattern = Pattern(pattern)
        self._value = None
        super(TimeVar, self).__init__(durations, self.move)

    def move(self):
        self._value = next(self.pattern)

    @property
    def value(self):
        return self._value
