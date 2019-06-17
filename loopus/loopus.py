from pythonosc import dispatcher, osc_server, udp_client
from threading import Thread

TICKS = 480


class Loopus:

    def __init__(self, host='127.0.0.1', in_port=9000, out_port=9002, verbose=False):
        self.dispatcher = dispatcher.Dispatcher()
        if verbose:
            self.dispatcher.set_default_handler(print)
        self.receiver = osc_server.ThreadingOSCUDPServer((host, in_port), self.dispatcher)
        self.sender = udp_client.SimpleUDPClient(host, out_port)
        self._bar = -1
        self._time_signature = (4,4)
        self.dispatcher.map('/bar', self.set_bar)
        self.dispatcher.map('/ts', self.set_time_signature)
        self.start()

    def start(self):
        t = Thread(target=self.receiver.serve_forever)
        t.daemon = True
        t.start()

    def set_bar(self, *args):
        self._bar = args[1]

    def set_time_signature(self, *args):
        self._time_signature = (args[1], args[2])

    @property
    def bar(self):
        return self._bar

    @property
    def next_bar(self):
        return self.bar + 1

    @property
    def time_signature(self):
        return self._time_signature

    @property
    def beat_per_bar(self):
        # todo: suppose that the beat unit is 4
        return self._time_signature[0]

    @property
    def beat_unit(self):
        return self._time_signature[1]

    def play(self, pitch, vel=100, dur=1.0, delay=0):
        when = (self.next_bar * self.beat_per_bar) + delay
        self.sender.send_message('/seq', [when, 'play', pitch, vel, int(dur*TICKS)])


if __name__ == '__main__':
    L = Loopus(verbose=True)

    key = input()
    while key != 'q':
        print(L.time_signature)
        try:
            d = int(key)
            for i in range(8):
                L.play(60, 80, 0.5, delay=2*i)
                L.play(62, 120, delay=2*i+ 1)
        except:
            L.sender.send_message('/hello', 'world')

        key = input()
    print("goodbye!")
