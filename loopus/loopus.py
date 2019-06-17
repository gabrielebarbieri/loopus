from pythonosc import dispatcher, osc_server, udp_client
from threading import Thread

TICKS = 480


class Loopus:

    def __init__(self, host='127.0.0.1', in_port=9000, out_port=9001, verbose=False):
        self.dispatcher = dispatcher.Dispatcher()
        if verbose:
            self.dispatcher.set_default_handler(print)
        self.receiver = osc_server.ThreadingOSCUDPServer((host, in_port), self.dispatcher)
        self.sender = udp_client.SimpleUDPClient(host, out_port)
        self._bar = -1
        self._time_signature = (4,4)
        self._callbacks = {}
        self.dispatcher.map('/bar', self.set_bar)
        self.dispatcher.map('/ts', self.set_time_signature)
        self.dispatcher.map('/callback', self.execute_callback)
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

    def play(self, when, pitch, vel=100, dur=1.0):
        self.sender.send_message('/seq', [when, 'play', pitch, vel, int(dur*TICKS)])

    def callback(self, when, func, *args):
        callback = (func, args)
        callback_id = str(id(callback))
        self._callbacks[callback_id] = callback
        self.sender.send_message('/seq', [when, 'callback', callback_id])

    def execute_callback(self, *args):
        callback = self._callbacks[args[1]]
        func = callback[0]
        c_args = callback[1]
        func(*c_args)


if __name__ == '__main__':
    L = Loopus(verbose=True)

    def loop(beat):
        L.play(beat, 60, 80, 0.5)
        L.play(beat + 1, 62, 120)
        L.callback(beat + 1.9, loop, beat + 2)


    key = input()
    while key != 'q':
        if key == 'c':
            L.callback(L.next_bar * L.beat_per_bar, sum, 12, 13)
        try:
            d = int(key)
            loop(L.next_bar * L.beat_per_bar)
        except:
            L.sender.send_message('/hello', 'world')

        key = input()
    print("goodbye!")
