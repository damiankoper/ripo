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
from ..config.VideoConfig import VideoConfig
from ..config.BallConfig import BallConfig
from ..config.CueConfig import CueConfig
from ..events import Event

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


class VideoProcessor:

    def __init__(self, config: VideoConfig):

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

        self.initFrameProcessing = InitialFrameProcessing(self.config.initTime, self.config.boundaries)

        frameWidth = Value('i', 1)
        frameHeight = Value('i', 1)

        ballConfig = BallConfig(self.config.width, self.config.height, frameWidth, frameHeight)
        cueConfig = CueConfig(self.config.width, self.config.height, frameWidth, frameHeight)

        sharedArray = RawArray(
            np.ctypeslib.as_ctypes_type(np.uint8), self.config.get_shape())
        frameValue = np.frombuffer(
            sharedArray, dtype=np.uint8).reshape(self.config.get_shape())

        self.ballProcess = BallProcessor(
            self.ballsQueue, self.throttle, sharedArray, self.frameReadLock, ballConfig, self.eventQueueBP)
        self.cueProcess = CueProcessor(
            self.cueQueue, self.throttle, sharedArray, self.frameReadLock, cueConfig, self.eventQueueCP)
        self.outputModuleProcess = OutputModule(
            self.ballsQueue, self.cueQueue, self.eventQueueVP, self.eventQueueBP, self.eventQueueCP, self.config.webPort)


        self.ballProcess.start()
        # Póki nie ma implementacji nie może kręcić się na sucho
        #self.cueProcess.start()
        self.outputModuleProcess.start()

        try:
            self.vcap = cv2.VideoCapture(
                "udp://0.0.0.0:"+str(self.config.udpPort), cv2.CAP_FFMPEG)
            while(1):
                self.vcap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
                ret, frame = self.vcap.read()


                if frame is not None:
                    cv2.imshow('VP: ORIGINAL', frame)
                    c = cv2.waitKey(1)

                    self.initFrameProcessing.on_frame(frame)
                    self.initFrameProcessing.display_components(False)

                    w, h = self.initFrameProcessing.get_pool_size()
                    frame = self.initFrameProcessing.get_warped_masked_frame()

                    frame = frame.flatten()
                    frame = np.resize(frame, self.config.get_shape())

                    #chwilowe, bo wywala się gdy podczas wykrywania stołu jest ten fragment nagrania bez stołu
                    if w < 500 or h < 200:
                        continue
                    with self.frameReadLock:
                        frameWidth.value = w
                        frameHeight.value = h
                        np.copyto(frameValue, frame.flatten())


                    self.throttle.get()
                    self.throttle.task_done()

                    #do włączenia po odpaleniu CP
                    #self.throttle.get()
                    #self.throttle.task_done()


        except (KeyboardInterrupt, SystemExit):
            self.terminate()
            self.cleanup()
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
            self.event = self.eventQueueVP.get_nowait()

            if self.event.eventType is "resetInit":
                self.initFrameProcessing.averaging_time = self.config.initTime


    def cleanup(self):
        if self.vrec is not None:
            self.vrec.release()
        if self.vcap is not None:
            self.vcap.release()

    def terminate(self):
        self.ballProcess.terminate()
        self.ballProcess.join()

        #self.cueProcess.terminate()
        #self.cueProcess.join()

        self.outputModuleProcess.terminate()
        self.outputModuleProcess.join()
