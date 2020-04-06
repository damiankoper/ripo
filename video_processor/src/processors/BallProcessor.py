import time
from enum import Enum

import cv2
import numpy as np
import imutils
from collections import deque

from .FrameProcessor import FrameProcessor
from ..pool_state.Ball import Ball, BallType
from ..pool_state.Vector2i import Vector2i


class BallProcessor(FrameProcessor):


    def eventHandling(self):
         while not self.eventQueue.empty():
            self.event = self.eventQueue.get_nowait()

            ####
    def run(self):
        try:
            self._run()
        except(KeyboardInterrupt, SystemExit):
            print("BP: Interrupt")
        print("BP: Exit")

    def _run(self):
        while(1):
            self.throttle.put(1)

            self.eventHandling()

            self.throttle.join()

            with self.lock:
                frame = np.frombuffer(self.frameValue, dtype=np.uint8)
                frameAvg = np.frombuffer(self.frameAvgValue, dtype=np.uint8)

                self.width = self.config.afterCutWidth.value
                self.height = self.config.afterCutHeight.value

            frame = np.resize(frame, self.width*self.height*3)
            frame = frame.reshape(self.height, self.width, 3)

            frameAvg = np.resize(frameAvg, self.width*self.height*3)
            frameAvg = frameAvg.reshape(self.height, self.width, 3)
                

            frameSubtracted = cv2.cvtColor(cv2.subtract(~frame, ~frameAvg), cv2.COLOR_BGR2GRAY)
            + cv2.cvtColor(cv2.subtract(frame, frameAvg), cv2.COLOR_BGR2GRAY)

    
            cv2.imshow('BP: DETECTED', frameSubtracted)
            cv2.imshow('BP: AVG FRAME', frame)
            cv2.waitKey(1)

            #if circles is not None:
            #    balls = []
            #    for n in circles[0]:
            #        balls.append(Ball(len(balls)+1, self.normalizeCoordinates(
            #        (n[0], n[1])), BallType.SOLID))

            #    self.queue.put(balls)
            
