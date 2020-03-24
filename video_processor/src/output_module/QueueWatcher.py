from threading import Thread, Lock
from multiprocessing import Queue
from .WebsocketServer import WebsocketServer
import asyncio


class QueueWatcher(Thread):
    def __init__(self, queue: Queue, list: list, lock: Lock, server: WebsocketServer, loop):
        Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.list = list
        self.server = server

        self.loop = loop

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self._run())

    async def _run(self):
        while 1:
            value = self.queue.get()
            with self.lock:
                self.list[:] = value
                self.server.poolState.balls = self.list
                await self.server.emitPoolState()
                await self.server.sio.sleep(0)
