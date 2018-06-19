from threading import Thread
import asyncio
from queue import PriorityQueue
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
        self.q = PriorityQueue()
        self.scheduled_events = {}
        self.sleeping_time = 0.0001
        self.latencies = []
        self.running = False

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
        new_loop = asyncio.new_event_loop()
        t = Thread(target=self.start_loop, args=(new_loop,))
        t.start()
        return t

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._async_run())

    def stop(self):
        self.running = False

    async def _async_run(self):
        self.running = True
        while self.running:
            if self.q.queue:
                beat = self.q.queue[0]
                latency = self.beat - beat
                if latency >= 0:
                    for f in self.scheduled_events[beat]:
                        f()
                        logging.debug(f' | beat {beat:>8.4f} | latency {latency:.6f} | event: {f.__name__:<10}')
                    # heappop(self.heap_queue)
                    self.q.get(block=False)
                    self.latencies.append(latency)
            asyncio.sleep(self.sleeping_time)

    def schedule(self, beat, f, *args, **kwargs):

        partial_f = functools.partial(f, *args, **kwargs)
        functools.update_wrapper(partial_f, f)
        try:
            self.scheduled_events[beat].append(partial_f)
        except KeyError:
            self.q.put(beat)
            self.scheduled_events[beat] = [partial_f]

    def schedule_at_next_bar(self, f, *args, **kwargs):
        self.schedule(self.next_bar, f, *args, **kwargs)


link_loop = LinkLoop()
link_loop.run()
