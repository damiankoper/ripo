import json
import time
from multiprocessing import Process, Queue
from threading import Lock, Thread

import eventlet
import socketio

from .QueueWatcher import QueueWatcher
from ..pool_state.PoolState import PoolState
from .WebsocketServer import WebsocketServer


class OutputModule(Process):

    def __init__(self, ballsQueue: Queue, cueQueue: Queue, port=8888):
        Process.__init__(self)
        self.ballsQueue = ballsQueue
        self.cueQueue = cueQueue

        self.poolStateLock = Lock()
        self.poolState = PoolState()

        self.port = port

    def run(self):
        websocketServer = WebsocketServer(
            self.poolState, self.port, self.poolStateLock)
        ballQueueWatcher = QueueWatcher(
            self.ballsQueue, self.poolState.balls, self.poolStateLock, websocketServer)

        # cueQueueWatcher = QueueWatcher(
        #    self.cueQueue, self.poolState.cues, self.poolStateLock, websocketServer)

        websocketServer.start()
        ballQueueWatcher.start()
        # cueQueueWatcher.start()

        websocketServer.join()
        ballQueueWatcher.join()
        # cueQueueWatcher.join()
