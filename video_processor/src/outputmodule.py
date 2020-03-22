from multiprocessing import Process, Queue
import eventlet
from threading import Thread, Lock
import socketio
import time
import json

# Zrób folder output_module i porozdzielaj proszę klasy do osobnych plików

# front też słucha na porcie 8888 więc domyślnie juz działa wszystko, tylko ważne jest teraz to mapowanie pozycji na przedział <0;1> bo nic nie zobaczysz


class PoolState():
    # KLASA PoolState jest TESTOWA DO TESTÓW, TRZEBA JĄ ZMIANIEĆ NA TĄ ZAIMPORTOWANĄ z folderi pool_state
    def __init__(self):
        self.balls = []
        self.cues = []

        self.sentAt = time.time()

    def toJson(self):
        # Tutaj w normalnym obiekcie musi wyjść sparsowany string json
        # testowo na środku powinna być zielona bila 6
        return {'balls': [{'position': {'x': 0.5, 'y': 0.5}, 'type': 'SOLID', 'number': 6}], 'cues': []}


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
            with self.lock:
                self.list[:] = value
            self.server.emitPoolState()


class OutputModule(Process):

    def __init__(self, ballsQueue, cueQueue, port=8888):
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
