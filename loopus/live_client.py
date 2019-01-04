from pythonosc import udp_client


client = udp_client.SimpleUDPClient('127.0.0.1', 9001)


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
    c.set_notes(notes)
    # input('play any key to stop')
    c.stop()

    # client.send_message('/live/browser/list', 'query')

    # c.stop()
    # client.send_message("/live/clip/stop", [1, 0])
    # client.send_message('/live/clip/state', [1, 0])

    # notes = [1, 0, 52, 0.5, 0.5, 100, 0, 52, 1.5, 0.5, 100, 0, 52, 2.5, 0.5, 100, 0, 52, 3.5, 0.5, 100, 0, 55, 0.0, 1.0,
    #          100, 0, 55, 1.0, 1.0, 100, 0,
    #          57, 2.0, 1.0, 100, 0, 59, 3.0, 1.0, 100, 0]
    # client.send_message('/live/clip/notes/add', notes)
