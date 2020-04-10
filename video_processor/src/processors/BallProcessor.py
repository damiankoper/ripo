import time
from enum import Enum

import cv2
import numpy as np
import math
from .FrameProcessor import FrameProcessor
from ..pool_state.Ball import Ball, BallType
from ..pool_state.Vector2i import Vector2i

from ..events.BallThresholdChangeEvent import BallThresholdChangeEvent
from ..events.BallLowerRadiusChangeEvent import BallLowerRadiusChangeEvent
from ..events.BallUpperRadiusChangeEvent import BallUpperRadiusChangeEvent


class BallProcessor(FrameProcessor):

    def eventHandling(self):
        while not self.eventQueue.empty():
            event = self.eventQueue.get_nowait()
            print("BP: ", event.eventType)
            if isinstance(event, BallThresholdChangeEvent):
                self.config.threshold = int(event.threshold)
            elif isinstance(event, BallUpperRadiusChangeEvent):
                self.config.radiusUpper = int(event.radius)
            elif isinstance(event, BallLowerRadiusChangeEvent):
                self.config.radiusLower = int(event.radius)

    def run(self):
        try:
            self._run()
        except(KeyboardInterrupt, SystemExit):
            print("BP: Interrupt")
        print("BP: Exit")

    def _run(self):

        sharp_kernel = np.array([[-1, -1, -1],
                                 [-1, 9, -1],
                                 [-1, -1, -1]])
        open_kernel = np.ones((3, 3), np.uint8)
        close_kernel = np.ones((3, 3), np.uint8)

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

            frameAvg = cv2.GaussianBlur(frameAvg, (5, 5), 0)
            frameAvg = cv2.filter2D(frameAvg, -1, sharp_kernel)

            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            frame = cv2.filter2D(frame, -1, sharp_kernel)

            difference = cv2.absdiff(frameAvg, frame)
            difference =cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(
                difference, self.config.threshold, 255, cv2.THRESH_BINARY)

            threshBefore = thresh

            iterations = 1
            thresh = cv2.morphologyEx(
                thresh, cv2.MORPH_OPEN, open_kernel, iterations=iterations)
            thresh = cv2.morphologyEx(
                thresh, cv2.MORPH_CLOSE, close_kernel, iterations=iterations)
           
            circles = []
            cnts = cv2.findContours(
                thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            count = 0
            for c in cnts:
                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                ratio = w/h
                ((x, y), r) = cv2.minEnclosingCircle(c)
                circleArea = math.pi * (r**2)
                if area > circleArea*0.5 and r < self.config.radiusUpper and r > self.config.radiusLower:
                    cv2.circle(frame, (int(x), int(y)), int(r),
                            (0, 255, 255), 2)
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    circles.append((int(x), int(y)))
                    count += 1

            cv2.imshow('BP: DETECTED', frame)
            cv2.imshow('BP: DIFF', difference)
            cv2.imshow('BP: THRESH', thresh)
            cv2.imshow('BP: THRESH BEFORE', threshBefore)
            cv2.imshow('BP: AVG FRAME', frameAvg)

            cv2.waitKey(1)

            if circles is not None:
                balls = []
                for n in circles:
                    balls.append(Ball(len(balls)+1, self.normalizeCoordinates(
                        (n[0], n[1])), BallType.SOLID))

                self.queue.put(balls)
