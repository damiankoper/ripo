import time
from enum import Enum

import cv2
import numpy as np

from .FrameProcessor import FrameProcessor
from ..pool_state.Ball import Ball, BallType
from ..pool_state.Vector2i import Vector2i


class BallProcessor(FrameProcessor):


    def eventHandling(self):
         while not self.eventQueue.empty():
            self.event = self.eventQueue.get_nowait()

            ####

    def run(self):
        while(1):
            self.throttle.put(1)

            self.eventHandling()

            self.throttle.join()

            with self.lock:
                frame = np.frombuffer(self.frameValue, dtype=np.uint8)

                self.width = self.config.afterCutWidth.value
                self.height = self.config.afterCutHeight.value

            frame = np.resize(frame, self.width*self.height*3)
            frame = frame.reshape(self.height, self.width, 3)

                

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,
            1, 20, param1=50, param2=30, minRadius=8, maxRadius=15)


            if circles is not None:
                for n in circles[0]:
                    cv2.circle(frame, (n[0], n[1]), n[2], (255, 0, 0))

            cv2.imshow('VIDEO', frame)
            c = cv2.waitKey(1)

            if circles is not None:
                balls = []
                for n in circles[0]:
                    balls.append(Ball(len(balls)+1, self.normalizeCoordinates(
                    (n[0], n[1])), BallType.SOLID))

                self.queue.put(balls)
            
