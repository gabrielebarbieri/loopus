from loopus.link_loop import link_loop
from loopus.midi import Player, Note
import signal

def handle_exit(s, frame):
    Note.release_all()
    link_loop.stop()
    import sys
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)


__ALL__ = [Player]