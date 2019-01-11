from pythonosc import udp_client
from pythonosc import dispatcher, osc_server
import threading
from queue import Queue
import time

client = udp_client.SimpleUDPClient('127.0.0.1', 9001)


class Receiver(object):

    def __init__(self, verbose=False):
        self.dispatcher = dispatcher.Dispatcher()
        if verbose:
            self.dispatcher.set_default_handler(print)
        self.server = osc_server.ThreadingOSCUDPServer(('127.0.0.1', 9000), self.dispatcher)

    def run_server(self):
        t = threading.Thread(target=self.server.serve_forever)
        t.start()

    def stop_server(self):
        self.server.shutdown()


receiver = Receiver(True)


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

    def __init__(self, track, scene):
        self.track = track
        self.scene = scene

    @property
    def osc_value(self):
        return [self.track, self.scene]

    def play(self):
        client.send_message('/live/clip/play', self.osc_value)

    def stop(self):
        client.send_message('/live/clip/stop', self.osc_value)

    def add_notes(self, notes):
        msg = sum((n.osc_value for n in notes), self.osc_value)
        client.send_message('/live/clip/notes/add', msg)

    def set_notes(self, notes):
        msg = sum((n.osc_value for n in notes), self.osc_value)
        client.send_message('/live/clip/notes/set', msg)
        pass


class Track(object):

    def __init__(self, track_id, receiver):

        self.track_id = track_id
        self.clips = []
        self.receiver = receiver
        self.receiver.dispatcher.map('/live/track/state', self.clip_changed)
        self.q = Queue()

    def clip_changed(self, *args):
        print(args)
        track_id = args[1]
        if track_id == self.track_id:
            self.q.put(args)

    def create_clip(self, notes, length):
        scene = len(self.clips)
        client.send_message('/live/clip/delete', [self.track_id, scene])
        client.send_message('/live/clip/create', [self.track_id, scene, length])
        c = Clip(self.track_id, scene)
        c.set_notes(notes)
        self.clips.append(c)
        time.sleep(0.1)
        c.play()

    def _play(self, loop_iterator):
        for loop in loop_iterator:
            self.create_clip(loop, 4)
            print(self.q.get())
        self.clips[-1].stop()

    def play(self, loop_iterator):
        t = threading.Thread(target=self._play, args=(loop_iterator,))
        t.start()


if __name__ == "__main__":

    receiver.run_server()

    client.send_message('/live/play', 'query')

    def get_bass(bass):
        return [Note(bass - 12, i+0.5, 1) for i in range(4)]


    notes = [Note(p, i, 1.) for i, p in enumerate([55, 55, 57, 59])]

    basses = [52, 50, 48, 48]
    # receiver.dispatcher.set_default_handler(print)
    Track(0, receiver).play([notes] * 4)
    Track(1, receiver).play(get_bass(bass) for bass in basses)
    input()
    client.send_message('/live/stop', 'query')
    receiver.stop_server()

