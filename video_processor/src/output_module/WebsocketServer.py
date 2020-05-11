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
from ..events.InitDurationChangeEvent import InitDurationChangeEvent
from ..events.PoolColorsChangeEvent import PoolColorsChangeEvent
from ..events.RerunInitRequestEvent import RerunInitRequestEvent
from ..events.BallThresholdChangeEvent import BallThresholdChangeEvent
from ..events.BallLowerRadiusChangeEvent import BallLowerRadiusChangeEvent
from ..events.BallUpperRadiusChangeEvent import BallUpperRadiusChangeEvent
from ..events.BalldpChangeEvent import BalldpChangeEvent
from ..events.BallMinDistChangeEvent import BallMinDistChangeEvent
from ..events.BallParam1ChangeEvent import BallParam1ChangeEvent
from ..events.BallParam2ChangeEvent import BallParam2ChangeEvent
from ..events.Event import Event


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
        await self.sio.emit('poolState', self.poolState.toJson())
        await self.sio.sleep(0)

    def initEventWatchers(self):
        @self.sio.event
        def connect(sid, environ):
            print("connect ", sid)

        @self.sio.event
        def initDurationChange(sid, data):
            setInitConf = InitDurationChangeEvent(data)
            self.handleEvent(setInitConf)

        @self.sio.event
        def poolColorsChange(sid, data):
            setInitConf = PoolColorsChangeEvent(data)
            self.handleEvent(setInitConf)

        @self.sio.event
        def rerunInitRequest(sid):
            self.handleEvent(RerunInitRequestEvent())

        @self.sio.event
        def ballThresholdChange(sid, data):
            setBallConf = BallThresholdChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def ballUpperRadiusChange(sid, data):
            setBallConf = BallUpperRadiusChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def ballLowerRadiusChange(sid, data):
            setBallConf = BallLowerRadiusChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def balldpChange(sid, data):
            setBallConf = BalldpChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def ballMinDistChange(sid, data):
            setBallConf = BallMinDistChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def ballParam1Change(sid, data):
            setBallConf = BallParam1ChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def ballParam2Change(sid, data):
            setBallConf = BallParam2ChangeEvent(data)
            self.handleEvent(setBallConf)

        @self.sio.event
        def disconnect(sid):
            print('disconnect ', sid)

    def handleEvent(self, event):
        print("OM: ", event.eventType)
        self.loadToQueue(event)
