from pythonosc import udp_client
from pythonosc import dispatcher, osc_server
import threading
from queue import Queue


client = udp_client.SimpleUDPClient('127.0.0.1', 9001)


class Receiver(object):

    def __init__(self):
        self.dispatcher = dispatcher.Dispatcher()
        # self.dispatcher.set_default_handler(print)
        self.dispatcher.map('/live/clip/state', self.receive)
        self.server = osc_server.ThreadingOSCUDPServer(('127.0.0.1', 9000), self.dispatcher)
        self.q = Queue()

    def receive(self, *args):
        print(*args)
        state = args[3]
        if state == 2: # clip is_playing
            self.q.put(args)

    def run_server(self):
        t = threading.Thread(target=self.server.serve_forever)
        t.start()

    def stop_server(self):
        self.server.shutdown()


receiver = Receiver()


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
        print(msg)
        client.send_message('/live/clip/notes/set', msg)
        pass


def create_clip(track, scene, notes, length):
    client.send_message('/live/clip/delete', [track, scene])
    client.send_message('/live/clip/create', [track, scene, length])
    c = Clip(track, scene)
    c.set_notes(notes)
    c.play()


if __name__ == "__main__":

    receiver.run_server()

    def get_notes(bass):
        notes = [Note(p, i, 1.) for i, p in enumerate([55, 55, 57, 59])]
        for i in range(4):
            notes.append(Note(bass - 12, i+0.5, 1))
        return notes

    basses = [52, 50, 48, 48, 48]

    def play(clip=0):
        create_clip(0, clip, get_notes(basses[clip]), 4)
        print(receiver.q.get())
        if clip + 1 < len(basses):
            play(clip+1)

    play()

    client.send_message('/live/stop', 'query')
    receiver.stop_server()
