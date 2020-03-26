import time
from threading import Lock, Thread
import json
import eventlet
import socketio
from flask import Flask
import logging
from aiohttp import web
import asyncio
# from ..pool_state.PoolState import PoolState


class WebsocketServer():
    def __init__(self, poolState, port, lock: Lock):
        Thread.__init__(self)

        self.port = port
        self.lock = lock
        self.sio = socketio.AsyncServer(
            async_mode='aiohttp', cors_allowed_origins="*")
        self.app = web.Application()
        self.sio.attach(self.app)

        self.poolState = poolState

        @self.sio.event
        def connect(sid, environ):
            print("connect ", sid)

        @self.sio.event
        def disconnect(sid):
            print('disconnect ', sid)

    def run(self):
        web.run_app(self.app, port=self.port)

    async def emitPoolState(self):
        self.poolState.sentAt = time.time()
        # print("Emitting")
        await self.sio.emit('poolState', self.poolState.toJson())
