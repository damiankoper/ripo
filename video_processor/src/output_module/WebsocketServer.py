import time
from threading import Lock, Thread

import eventlet
import socketio

from ..pool_state.PoolState import PoolState


class WebsocketServer(Thread):
    def __init__(self, poolState: PoolState, port, lock: Lock):
        Thread.__init__(self)

        self.port = port
        self.lock = lock
        self.sio = socketio.Server(cors_allowed_origins="*")
        self.app = socketio.WSGIApp(self.sio)

        self.poolState = poolState

        @self.sio.event
        def connect(sid, environ):
            print("Client connected: ", sid)

        @self.sio.event
        def disconnect(sid, environ):
            print("Client disconnected: ", sid)

    def run(self):
        eventlet.wsgi.server(eventlet.listen(
            ('', self.port)), self.app)

    def emitPoolState(self):
        with self.lock:
            self.poolState.sentAt = time.time()
            self.sio.emit('poolState', self.poolState.toJson())
