from aiohttp import web
import json
import time
from multiprocessing import Process, Queue
from threading import Lock, Thread
import signal

import eventlet
import socketio

from .QueueWatcher import QueueWatcher
from ..pool_state.PoolState import PoolState
from .WebsocketServer import WebsocketServer
import asyncio


class OutputModule(Process):

    def __init__(self, ballsQueue: Queue, cueQueue: Queue, eventQueueVP: Queue,
    eventQueueBP: Queue, eventQueueCP: Queue, port=8888):
        Process.__init__(self, daemon=True)
        self.ballsQueue = ballsQueue
        self.cueQueue = cueQueue

        self.eventQueueVP = eventQueueVP
        self.eventQueueBP = eventQueueBP
        self.eventQueueCP = eventQueueCP

        self.poolStateLock = Lock()
        self.poolState = PoolState()

        self.port = port
        self.websocketServer = None

    def run(self):
        loop = asyncio.new_event_loop()
        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame), self.cleanup)
        asyncio.set_event_loop(loop)

        self.websocketServer = WebsocketServer(
            self.poolState, self.port, self.poolStateLock, self.eventQueueVP, 
            self.eventQueueBP, self.eventQueueCP)
        ballQueueWatcher = QueueWatcher(
            self.ballsQueue, self.poolState.balls, self.poolStateLock, self.websocketServer,  loop)

        # cueQueueWatcher = QueueWatcher(
        #    self.cueQueue, self.poolState.cues, self.poolStateLock, self.websocketServer)

        ballQueueWatcher.start()
        # cueQueueWatcher.start()

        try:
            self.websocketServer.run()
        except(KeyboardInterrupt, SystemExit):
            print("OM: Interrupt")
        print("OM: Exit")

    def cleanup(self):
        print("cleanup")
        self.websocketServer.app.shutdown()
        self.websocketServer.app.cleanup()