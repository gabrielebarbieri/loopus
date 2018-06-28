from loopus.clock import clock
from loopus.midi import Player, Note
import signal


def handle_exit(s, frame):
    Note.release_all()
    clock.stop()
    import sys
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)


__ALL__ = [Player]
