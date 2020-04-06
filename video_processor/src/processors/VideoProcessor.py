import argparse
import cProfile
import ctypes
import os
import sys
import time
from multiprocessing import Array, Lock, Queue, RawArray, Value, JoinableQueue

import cv2
import numpy as np

from .BallProcessor import BallProcessor
from .CueProcessor import CueProcessor
from ..output_module.OutputModule import OutputModule
from .InitialFrameProcessing import InitialFrameProcessing
from ..config.VideoProcessorConfig import VideoProcessorConfig
from ..config.BallProcessorConfig import BallProcessorConfig
from ..config.CueProcessorConfig import CueProcessorConfig
from ..events import Event
from ..events.RerunInitRequestEvent import RerunInitRequestEvent
from ..events.InitDurationChangeEvent import InitDurationChangeEvent
from ..events.PoolColorsChangeEvent import PoolColorsChangeEvent

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


class VideoProcessor:

    def __init__(self, config: VideoProcessorConfig):

        self.config = config

        self.ballsQueue = Queue()
        self.cueQueue = Queue()

        self.throttle = JoinableQueue()

        self.eventQueueVP = Queue()
        self.eventQueueBP = Queue()
        self.eventQueueCP = Queue()

        self.event = None

        self.vcap = None
        self.vrec = None

        self.frameReadLock = Lock()

        self.ballProcess = None
        self.cueProcess = None
        self.outputModuleProcess = None

        self.initFrameProcessing: InitialFrameProcessing = None

    def capture(self):

        self.initFrameProcessing = InitialFrameProcessing(self.config)

        frameWidth = Value('i', 1)
        frameHeight = Value('i', 1)

        ballProcessorConfig = BallProcessorConfig(
            self.config.width, self.config.height, frameWidth, frameHeight)
        cueProcessorConfig = CueProcessorConfig(
            self.config.width, self.config.height, frameWidth, frameHeight)

        sharedFrame = RawArray(
            np.ctypeslib.as_ctypes_type(np.uint8), self.config.get_flat_shape())
        sharedAvgFrame = RawArray(
            np.ctypeslib.as_ctypes_type(np.uint8), self.config.get_flat_shape())
        numpyFrame = np.frombuffer(
            sharedFrame, dtype=np.uint8).reshape(self.config.get_flat_shape())
        numpyAvgFrame = np.frombuffer(
            sharedAvgFrame, dtype=np.uint8).reshape(self.config.get_flat_shape())

        self.ballProcess = BallProcessor(
            self.ballsQueue,
            self.throttle,
            sharedFrame,
            sharedAvgFrame,
            self.frameReadLock,
            ballProcessorConfig,
            self.eventQueueBP
        )

        self.cueProcess = CueProcessor(
            self.cueQueue,
            self.throttle,
            sharedFrame,
            sharedAvgFrame,
            self.frameReadLock,
            cueProcessorConfig,
            self.eventQueueCP
        )

        self.outputModuleProcess = OutputModule(
            self.ballsQueue,
            self.cueQueue,
            self.eventQueueVP,
            self.eventQueueBP,
            self.eventQueueCP,
            self.config.webPort
        )

        self.ballProcess.start()
        # Póki nie ma implementacji nie może kręcić się na sucho
        # self.cueProcess.start()
        self.outputModuleProcess.start()

        try:
            self.vcap = cv2.VideoCapture(
                "udp://0.0.0.0:"+str(self.config.udpPort)+"?overrun_nonfatal=1", cv2.CAP_FFMPEG)
            self.vcap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

            while(1):
                self.eventHandling()
                ret, frame = self.vcap.read()
                if ret:
                    cv2.imshow('VP: ORIGINAL', frame)

                    self.initFrameProcessing.on_frame(frame)
                    self.initFrameProcessing.display_components()

                    w, h = self.initFrameProcessing.get_pool_size()

                    frame = self.initFrameProcessing.get_warped_frame().flatten()
                    frame = np.resize(frame, self.config.get_flat_shape())

                    avg_frame = self.initFrameProcessing.get_avg_frame().flatten()
                    avg_frame = np.resize(avg_frame, self.config.get_flat_shape())

                    # chwilowe, bo wywala się gdy podczas wykrywania stołu jest ten fragment nagrania bez stołu
                    if w < 500 or h < 500:
                        continue
                    with self.frameReadLock:
                        frameWidth.value = w
                        frameHeight.value = h
                        np.copyto(numpyFrame, frame)
                        np.copyto(numpyAvgFrame, avg_frame)

                    self.throttle.get()
                    self.throttle.task_done()

                # Main wait to refresh windows
                c = cv2.waitKey(1)

                # do włączenia po odpaleniu CP
                # self.throttle.get()
                # self.throttle.task_done()

        except (KeyboardInterrupt, SystemExit):
            print("VP: Interrupt")
            self.cleanup()
            self.terminate()
        print("VP: Exit")
        sys.exit(0)

    def record(self):
        try:
            self.vrec = cv2.VideoWriter(
                self.config.recordingPath, cv2.VideoWriter_fourcc(*'MP4V'),
                self.config.recordingFps, (self.config.width, self.config.height))

            self.vcap = cv2.VideoCapture(
                "udp://0.0.0.0:"+str(self.config.udpPort), cv2.CAP_FFMPEG)

            while(1):
                ret, frame = self.vcap.read()
                if frame is not None:
                    self.vrec.write(frame)
                    cv2.imshow('VIDEO', frame)
                    c = cv2.waitKey(1)
                    if c & 0xFF == ord('q'):
                        self.cleanup()
                        break

        except (KeyboardInterrupt, SystemExit):
            self.cleanup()
            sys.exit(0)

    def eventHandling(self):
        while not self.eventQueueVP.empty():
            event = self.eventQueueVP.get_nowait()
            print("VP: ", event.eventType)
            if isinstance(event, RerunInitRequestEvent):
                self.initFrameProcessing.reset_avg()
            elif isinstance(event, InitDurationChangeEvent):
                self.config.initDuration = int(event.initDuration)
            elif isinstance(event, PoolColorsChangeEvent):
                self.config.pool_color_range = event.pool_color_range

    def cleanup(self):
        if self.vrec is not None:
            self.vrec.release()
        if self.vcap is not None:
            self.vcap.release()
            

    def terminate(self):
        self.ballProcess.terminate()
        self.ballProcess.join()

        self.outputModuleProcess.kill()
        #self.outputModuleProcess.terminate()
        #self.outputModuleProcess.join()

        # self.cueProcess.terminate()
        # self.cueProcess.join()
