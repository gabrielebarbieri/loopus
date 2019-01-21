from pythonosc import udp_client
from pythonosc import dispatcher, osc_server
import threading
from queue import Queue
import time


class Live(object):

    def __init__(self, host='127.0.0.1', in_port=9000, out_port=9001, verbose=False):
        self.dispatcher = dispatcher.Dispatcher()
        if verbose:
            self.dispatcher.set_default_handler(print)
        self.receiver = osc_server.ThreadingOSCUDPServer((host, in_port), self.dispatcher)
        self.sender = udp_client.SimpleUDPClient(host, out_port)
        self.q = {}

    def run(self):
        t = threading.Thread(target=self.receiver.serve_forever)
        t.start()

    def shutdown(self):
        self.receiver.shutdown()

    def get(self, key, callback_key=None):
        if callback_key is None:
            callback_key = key
        try:
            q = self.q[callback_key]
        except KeyError:
            q = Queue()
            self.q[callback_key] = q
            self.dispatcher.map(callback_key, lambda *args: q.put(args))

        self.sender.send_message(key, 'query')
        return q.get()[1:]

    def play(self):
        self.sender.send_message('/live/play', 'query')

    def stop(self):
        self.sender.send_message('/live/stop', 'query')


class open_live:

    def __init__(self, host='127.0.0.1', in_port=9000, out_port=9001, verbose=False):
        self.host = host
        self.in_port = in_port
        self.out_port = out_port
        self.verbose = verbose
        self.live = None

    def __enter__(self):
        self.live = Live(self.host, self.in_port, self.out_port, self.verbose)
        self.live.run()
        return self.live

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print(exc_type)
        # print(exc_val)
        # print(exc_tb)
        if self.live is not None:
            self.live.shutdown()
        # print('exit')


class Note(object):

    def __init__(self, pitch, time, duration=1., velocity=100, mute=0):
        self.pitch = pitch
        self.time = time
        self.duration = duration
        self.velocity = velocity
        self.mute = mute

    @property
    def osc_value(self):
        return [self.pitch, self.time, self.duration, self.velocity, self.mute]

    def __repr__(self):
        return 'Note{}'.format(self.osc_value)


class Clip(object):

    def __init__(self, track, scene, length, sender):
        self.track = track
        self.scene = scene
        self.length = length
        self.sender = sender
        self.clear()
        self.create()

    @property
    def osc_value(self):
        return [self.track, self.scene]

    def send(self, key, msg=None):
        if msg is None:
            msg = self.osc_value
        self.sender.send_message(key, msg)

    def play(self):
        self.send('/live/clip/play')

    def stop(self):
        self.send('/live/clip/stop')

    def add_notes(self, notes):
        msg = sum((n.osc_value for n in notes), self.osc_value)
        self.send('/live/clip/notes/add', msg)

    def set_notes(self, notes):
        msg = sum((n.osc_value for n in notes), self.osc_value)
        self.send('/live/clip/notes/set', msg)

    def clear(self):
        self.send('/live/clip/delete')

    def create(self):
        self.send('/live/clip/create', self.osc_value + [self.length])


class Loop(object):

    def __init__(self, track, sender, receiver):

        self.track = track
        self.clips = []
        self.sender = sender
        self.receiver = receiver
        self.receiver.dispatcher.map('/live/track/state', self.clip_changed)
        self.q = Queue()

    def send(self, key, msg):
        self.sender.send_message(key, msg)

    def clip_changed(self, *args):
        track = args[1]
        if track == self.track:
            self.q.put(args)

    def play_clip(self, notes, length):
        scene = len(self.clips)
        c = Clip(self.track, scene, length=length, sender=self.sender)
        c.set_notes(notes)
        self.clips.append(c)
        time.sleep(0.1)
        c.play()

    def _play(self, loop_iterator):
        for loop in loop_iterator:
            self.play_clip(loop, 4)
            print(self.q.get())
        self.clips[-1].stop()

    def play(self, loop_iterator):
        t = threading.Thread(target=self._play, args=(loop_iterator,))
        t.start()



