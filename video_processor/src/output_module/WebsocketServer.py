import time
from threading import Lock, Thread
import json
import eventlet
import socketio
from flask import Flask
import logging

#from ..pool_state.PoolState import PoolState


class WebsocketServer(Thread):
    def __init__(self, poolState, port, lock: Lock):
        Thread.__init__(self)

        self.port = port
        self.lock = lock
        self.sio = socketio.Server(
            cors_allowed_origins="*", async_mode='threading')
        self.app = Flask(__name__)
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        self.poolState = poolState

        @self.sio.event
        def connect(sid, environ):
            print("Client connected: ", sid)

        @self.sio.event
        def disconnect(sid):
            print("Client disconnected: ", sid)

        @self.sio.event
        def dupka(sid, environ):
            print("dupka: ", sid)
            self.sio.emit('poolState', self.poolState.toJson())

    def run(self):
        self.app.run(threaded=True, host='0.0.0.0', port=self.port)

    def emitPoolState(self):
        self.poolState.sentAt = time.time()
        self.sio.emit('poolState', self.poolState.toJson())
