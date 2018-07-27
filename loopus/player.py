from loopus.midi import Note
from loopus.loop import Loop
from loopus.pattern import Pattern


class Player(Loop):

    def __init__(self, clock, scale, degrees, dur=None, sus=None, channel=0):
        if dur is None:
            dur = 1
        if sus is None:
            sus = dur
        self.channel = channel
        self.degrees = Pattern(degrees)
        self.sustains = Pattern(sus)
        self.scale = scale
        super(Player, self).__init__(clock, durations=dur, actions=None)

    def get_pitch(self, degree):
        return self.scale[degree].midi

    def play_note(self, beat, degree, dur=1.0, vel=100):
        pitch = self.get_pitch(degree)
        note = Note(pitch, channel=self.channel)
        self.clock.schedule(beat, note.play, vel)
        self.clock.schedule(beat + dur, note.release)

    def schedule_action(self, beat):
        # Need to override this method since play note already schedule playing and stopping a note
        self.play_note(beat, next(self.degrees), dur=next(self.sustains))


if __name__ == '__main__':
    from loopus.clock import Clock
    from loopus.scale import Scale
    from time import sleep
    c = Clock()
    s = Scale()

    c.start()
    p = Player(c, s, [4, 1, 0], dur=[0.5, 0.25, 0.25], sus=[0.25])
    p.play()
    sleep(5)
    p.stop()
    sleep(1)
    c.stop()
