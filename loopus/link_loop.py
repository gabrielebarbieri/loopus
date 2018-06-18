from gevent import monkey; monkey.patch_all()
import gevent
from heapq import heappop, heappush
from abletonlink import Link
import functools
import logging
from math import fmod

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class LinkLoop(object):

    def __init__(self, bpm=120, quantum=4):
        self.link = Link(bpm)
        self.quantum = quantum
        self.link.enable(True)
        self.clock = self.link.clock()
        self.heap_queue = []
        self.scheduled_events = {}
        self.sleeping_time = 0.0001
        self.latencies = []

    @property
    def beat(self):
        t = self.clock.micros()
        state = self.link.captureAppSessionState()
        return state.beatAtTime(t, self.quantum)

    @property
    def next_bar(self):
        beat = self.beat
        return beat + self.quantum - self.get_phase(beat)

    def get_phase(self, beat):
        return fmod(beat, self.quantum)

    def run(self):
        return gevent.spawn(self._run)

    def _run(self):
        while True:
            if self.heap_queue:
                beat = self.heap_queue[0]
                latency = self.beat - beat
                if latency >= 0:
                    for f in self.scheduled_events[beat]:
                        f()
                        logging.debug(f' | beat {beat:>8.4f} | latency {latency:.6f} | event: {f.__name__:<10}')
                    heappop(self.heap_queue)
                    self.latencies.append(latency)
            gevent.sleep(self.sleeping_time)

    def schedule(self, beat, f, *args, **kwargs):

        partial_f = functools.partial(f, *args, **kwargs)
        functools.update_wrapper(partial_f, f)
        try:
            self.scheduled_events[beat].append(partial_f)
        except KeyError:
            heappush(self.heap_queue, beat)
            self.scheduled_events[beat] = [partial_f]

    def schedule_at_next_bar(self, f, *args, **kwargs):
        self.schedule(self.next_bar, f, *args, **kwargs)


link_loop = LinkLoop()
link_loop.run()
