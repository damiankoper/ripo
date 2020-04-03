import time
from threading import Lock, Thread
import json
import eventlet
import socketio
from flask import Flask
import logging
from aiohttp import web
import asyncio
from multiprocessing import Queue
from ..events.SetInitConfigEvent import SetInitConfigEvent
from ..events.RerunInitRequestEvent import RerunInitRequestEvent
from ..events.Event import Event
# from ..pool_state.PoolState import PoolState


class WebsocketServer():
    def __init__(self, poolState, port, lock: Lock, eventQueueVP: Queue, eventQueueBP: Queue, eventQueueCP: Queue):
        Thread.__init__(self)

        self.eventQueueVP = eventQueueVP
        self.eventQueueBP = eventQueueBP
        self.eventQueueCP = eventQueueCP

        self.port = port
        self.lock = lock
        self.sio = socketio.AsyncServer(
            async_mode='aiohttp', cors_allowed_origins="*")
        self.app = web.Application()
        self.sio.attach(self.app)

        self.poolState = poolState

        self.initEventWatchers()
      
    def loadToQueue(self, event: Event):
        self.eventQueueVP.put(event)
        self.eventQueueBP.put(event)
        self.eventQueueCP.put(event)

    def run(self):
        web.run_app(self.app, port=self.port)
     

    async def emitPoolState(self):
        self.poolState.sentAt = time.time()
        # print("Emitting")
        await self.sio.emit('poolState', self.poolState.toJson())

    def initEventWatchers(self):
        @self.sio.event
        def connect(sid, environ):
            print("connect ", sid)

        @self.sio.event
        def setInitConfig(sid, data):
            data = json.load(data)
            setInitConf = SetInitConfigEvent("setInitConfig", data["time"])
            self.handleEvent(setInitConf)

        @self.sio.event
        def rerunInitRequest(sid):
            self.handleEvent(RerunInitRequestEvent())

        @self.sio.event
        def disconnect(sid):
            print('disconnect ', sid)

    def handleEvent(self, event):
        print("OM: ", event.eventType)
        self.loadToQueue(event)
