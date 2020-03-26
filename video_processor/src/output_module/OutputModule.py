from aiohttp import web
import json
import time
from multiprocessing import Process, Queue
from threading import Lock, Thread

import eventlet
import socketio

from .QueueWatcher import QueueWatcher
from ..pool_state.PoolState import PoolState
from .WebsocketServer import WebsocketServer
import asyncio


class OutputModule(Process):

    def __init__(self, ballsQueue: Queue, cueQueue: Queue, port=8888):
        Process.__init__(self)
        self.ballsQueue = ballsQueue
        self.cueQueue = cueQueue

        self.poolStateLock = Lock()
        self.poolState = PoolState()

        self.port = port

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        websocketServer = WebsocketServer(
            self.poolState, self.port, self.poolStateLock)
        ballQueueWatcher = QueueWatcher(
            self.ballsQueue, self.poolState.balls, self.poolStateLock, websocketServer,  loop)

        # cueQueueWatcher = QueueWatcher(
        #    self.cueQueue, self.poolState.cues, self.poolStateLock, websocketServer)

        ballQueueWatcher.start()

        websocketServer.run()
        websocketServer.app.shutdown()
        websocketServer.app.cleanup()
        # cueQueueWatcher.start()
        ballQueueWatcher.join()
        # cueQueueWatcher.join()
