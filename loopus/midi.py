import mido


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
