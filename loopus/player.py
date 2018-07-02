from loopus.midi import Note
from loopus.loop import Loop
from loopus.pattern import Pattern


class Player(Loop):

    def __init__(self, p, dur=None, sus=None, channel=0):
        if dur is None:
            dur = 1
        if sus is None:
            sus = dur
        self.channel = channel
        self.pitches = Pattern(p)
        self.sustains = Pattern(sus)
        super(Player, self).__init__(durations=dur, actions=None)

    def play_note(self, beat, pitch, dur=1.0, vel=100):
        note = Note(pitch, channel=self.channel)
        self.clock.schedule(beat, note.play, vel)
        self.clock.schedule(beat + dur, note.release)

    def schedule_action(self, beat):
        # Need to override this method since play note already schedule playing and stopping a note
        self.play_note(beat, next(self.pitches), dur=next(self.sustains))

if __name__ == '__main__':
    Player([67, 62, 62], dur=[0.5, 0.25, 0.25], sus=[0.25])
