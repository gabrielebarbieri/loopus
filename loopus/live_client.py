from pythonosc import udp_client
from pythonosc import dispatcher, osc_server
import threading
from queue import Queue


client = udp_client.SimpleUDPClient('127.0.0.1', 9001)


class Receiver(object):

    def __init__(self):
        self.dispatcher = dispatcher.Dispatcher()
        # self.dispatcher.set_default_handler(print)
        self.dispatcher.map('/live/clip/loopjump', self.receive)
        self.server = osc_server.ThreadingOSCUDPServer(('127.0.0.1', 9000), self.dispatcher)
        self.q = Queue()

    def receive(self, *args):
        self.q.put(args)

    def run_server(self):
        t = threading.Thread(target=self.server.serve_forever)
        t.start()

    def stop_server(self):
        self.server.shutdown()


receiver = Receiver()
receiver.run_server()


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

if __name__ == "__main__":

    notes = [Note(p, i, 1.) for i, p in enumerate([55, 55, 57, 59])]
    for i in range(4):
        notes.append(Note(52 - 12, i+0.5, 1))

    c = Clip(1, 0)
    c.play()
    import time
    time.sleep(0.1)

    client.send_message('/live/clip/loopjump', [1, 1])


    input('hello')
    #
    # Clip(1, 1).play()
    # print(receiver.q.get())
    # Clip(1, 0).play()
    # print(receiver.q.get())
    # Clip(1, 1).play()
    # print(receiver.q.get())
    # Clip(1, 0).play()
    # print(receiver.q.get())
    # Clip(1, 1).play()
    # print(receiver.q.get())




    # c = Clip(0, 0)
    # c.play()
    # import time
    # time.sleep(0.1)
    # c = Clip(1, 1)
    # c.play()



    # c.set_notes(notes)
    # input('play any key to stop')
    # c.stop()

    client.send_message('/live/stop', 'query')
    receiver.stop_server()

    # c.stop()
    # client.send_message("/live/clip/stop", [1, 0])
    # client.send_message('/live/clip/state', [1, 0])

    # notes = [1, 0, 52, 0.5, 0.5, 100, 0, 52, 1.5, 0.5, 100, 0, 52, 2.5, 0.5, 100, 0, 52, 3.5, 0.5, 100, 0, 55, 0.0, 1.0,
    #          100, 0, 55, 1.0, 1.0, 100, 0,
    #          57, 2.0, 1.0, 100, 0, 59, 3.0, 1.0, 100, 0]
    # client.send_message('/live/clip/notes/add', notes)
