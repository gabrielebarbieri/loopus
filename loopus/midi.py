import mido
from loopus.link_loop import LinkLoop


class Note(object):

    playing_notes = {}
    port = mido.open_output()

    def __init__(self, pitch, channel=0):
        self.playing = False
        self.pitch = pitch
        self.channel = channel
        self.id = (self.channel, self.pitch)

    def play(self, velocity=100):
        try:
            Note.playing_notes[self.id].release()
        except KeyError:
            pass
        self.playing = True
        Note.playing_notes[self.id] = self
        msg = mido.Message('note_on', note=self.pitch, channel=self.channel, velocity=velocity)
        self.port.send(msg)

    def release(self):
        if not self.playing:
            return
        msg = mido.Message('note_off', note=self.pitch, channel=self.channel)
        self.port.send(msg)
        self.playing = False

    @classmethod
    def release_all(cls):
        for note in cls.playing_notes.values():
            note.release()


class Player(LinkLoop):

    def play_note(self, beat, pitch, dur=1.0, vel=100, channel=0):
        note = Note(pitch, channel=channel)
        self.schedule(beat, note.play, vel)
        self.schedule(beat + dur, note.release)

    def play_sequence(self, beat, pitches):
        if pitches:
            self.play_note(beat, pitches[0])
            if len(pitches) > 1:
                self.schedule(beat, self.play_sequence, beat + 1, pitches[1:])
            else:
                self.schedule(beat, self.play_sequence, beat + 1, pitches)
