from threading import Thread, Lock
from multiprocessing import Queue
from concurrent.futures import ProcessPoolExecutor
from .WebsocketServer import WebsocketServer
import asyncio


class QueueWatcher(Thread):
    def __init__(self, queue: Queue, datalist: list, lock: Lock, server: WebsocketServer, loop, emit = True):
        Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.datalist = datalist
        self.server = server

        self.loop = loop
        self.emit = emit
        self.daemon = True

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self._run())

    async def _run(self):
        while 1:
            value = self.queue.get()
            with self.lock:
                if self.datalist != value:
                    self.datalist[:] = value
                    await self.server.emitPoolState()