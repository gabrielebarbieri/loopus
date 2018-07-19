from loopus.clock import Clock
from loopus.scale import Scale
from loopus.midi import Note
from loopus.player import Player


class Loopus(object):

    def __init__(self):
        self.clock = Clock()
        self.scale = Scale()
        self.loops = {}

    def start(self):
        self.clock.start()

    def stop_all(self):
        Note.release_all()
        self.clock.stop()

    def play(self, name, p, dur, sus):
        self.stop(name)
        p = Player(self.clock, self.scale, p, dur=dur, sus=sus)
        p.play()
        self.loops[name] = p

    def stop(self, name=None):
        if name is None:
            self.stop_all()
        else:
            try:
                self.loops[name].stop()
            except KeyError:
                pass


if __name__ == '__main__':
    l = Loopus()
    l.start()
    l.play('a', [0, 4, 2], dur=[0.5, 0.25, 0.25], sus=[0.25])
    from time import sleep
    sleep(5)
    l.stop()
