import mido
from loopus.link_loop import link_loop
from itertools import cycle
import signal
import sys


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


def play_note(beat, pitch, dur=1.0, vel=100, channel=0):
    note = Note(pitch, channel=channel)
    link_loop.schedule(beat, note.play, vel)
    link_loop.schedule(beat + dur, note.release)


class Player(object):

    def __init__(self, p, dur=None, sus=None, channel=0):
        self.channel = channel
        self.pitches = cycle(p)
        self.durations = cycle(dur if dur else [1])
        self.sustains = cycle(sus if sus else self.durations)
        self.running = False
        self.play_sequence(self.pitches, self.durations, self.sustains)

    def play_sequence(self, pitches, durations, sustains):
        self.running = True
        beat = link_loop.next_bar
        link_loop.schedule(beat, self.loop_sequence, pitches, durations, sustains, beat)

    def stop_sequence(self):
        self.running = False

    def loop_sequence(self, pitches, durations, sustains, beat):
        if self.running:
            dur = next(durations)
            play_note(beat, next(pitches), dur=next(sustains), channel=self.channel)
            link_loop.schedule(beat, self.loop_sequence, pitches, durations, sustains, beat + dur)


if __name__ == '__main__':
    Player([67, 62, 62], dur=[1, 0.5, 0.5], sus=[0.1])
