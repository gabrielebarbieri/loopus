from math import pi, cos
from random import random, choice
from loopus.live_client import Note, open_live, Loop


if __name__ == "__main__":
    s = [(4 + e) % 12 for e in [0, 2, 3, 5, 7, 8, 10]]

    def loop_on(l):
        i = 0
        t = len(l)
        while True:
            yield l[i % t]
            i += 1

    # basses = loop_on([52, 50, 48, 48])
    basses = [52, 50, 48, 48] * 2

    def left_hand(root):
        return [Note(root, i+0.5, 1) for i in range(4)] + [Note(p, i, 1.) for i, p in enumerate([55, 55, 57, 59])]


    def bassline(root):
        return [Note(root, 0, 3/2 * 0.25, 80), Note(root, 3/2, 0.25, 80), Note(root, 5/2, 3/2 * 0.6, 80)]


    kicks = [Note(36, i, 0.75) for i in range(4)] + [Note(36, i+0.75, 0.25, 80) for i in range(4)]


    def drum():
        hats = []
        for i in range(16):
            beat = i/4
            note = Note(choice([38, 42]), beat, 1/4, cosr(beat, 60, 50, choice([7/3, 5/2])))
            hats.append(note)
        return kicks + hats

    def cosr(beat, a1, a2, a3):
        return a1 + a2 * cos(2 * pi * a3 * beat)

    def quantize(note, scale):
        n = int(note)
        if n % 12 in scale:
            return n
        for i in range(1, 12):
            if (n + i) % 12 in scale:
                return n + i
            if (n - i) % 12 in scale:
                return n - i

    def right_hand(beat, root, scale, dur=1/4):
        b = beat
        notes = []
        while b - beat < 4:
            pitch = quantize(cosr(beat, root + 24, cosr(b, 5, 3, 1 / 2), 7 / 3), scale)
            v = cosr(b, 80, 20, 7 / 3)
            notes.append(Note(pitch=pitch, time=b - beat, duration=2*dur, velocity=v))
            b += dur

        return notes


    def lead(beat, root, scale, dur=1/4):
        b = beat
        notes = []
        while b - beat < 4:
            if random() > 0.6:
                pitch = quantize(cosr(beat, root + 24, cosr(b, 5, 3, 1 / 2), 7 / 3) + 7, scale)
                v = cosr(b, 80, 20, 7 / 3) - 60
                notes.append(Note(pitch=pitch, time=b - beat, duration=2*dur, velocity=v))
            b += dur

        return notes

    with open_live(verbose=True) as li:
        li.play()
        Loop(0, li.sender, li.receiver).play(left_hand(bass) for bass in basses)
        Loop(1, li.sender, li.receiver).play(right_hand(4 * i, b, s) for i, b in enumerate(basses))
        Loop(2, li.sender, li.receiver).play(drum() for _ in basses)
        Loop(3, li.sender, li.receiver).play(lead(4 * i, b, s) for i, b in enumerate(basses))
        Loop(4, li.sender, li.receiver).play(bassline(b) for b in basses)
        input()
        li.stop()
