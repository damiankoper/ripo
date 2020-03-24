from threading import Thread, Lock
from multiprocessing import Queue
from .WebsocketServer import WebsocketServer


class QueueWatcher(Thread):
    def __init__(self, queue: Queue, list: list, lock: Lock, server: WebsocketServer):
        Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.list = list
        self.server = server

    def run(self):
        while 1:
            value = self.queue.get()
            # print(value)
            with self.lock:
                self.list[:] = value
                self.server.poolState.balls = self.list
                self.server.emitPoolState()
