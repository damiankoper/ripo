import time
from enum import Enum

import cv2
import numpy as np

from .FrameProcessor import FrameProcessor
from ..pool_state.Ball import Ball, BallType


class BallProcessor(FrameProcessor):

    def run(self):
        while(1):
            with self.lock:
                frame = np.frombuffer(self.frameValue, dtype=np.uint8)
                frame = frame.reshape(self.height, self.width, 3)
            if not np.all(frame == 0):
                    while(1):
                        with self.lock:
                            frame = np.frombuffer(self.frameValue, dtype=np.uint8)
                            frame = frame.reshape(self.height, self.width, 3)

                        time_s = time.perf_counter()

                        imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        width = frame.shape[1]
                        height = frame.shape[0]

                        boundaries = [
                        ([70, 150, 50], [95, 255, 220]),
                        ]

                        for (lower, upper) in boundaries:
                            lower = np.array(lower, dtype="uint8")
                            upper = np.array(upper, dtype="uint8")

                            mask = cv2.inRange(imageHSV, lower, upper)
                            output = cv2.bitwise_and(frame, frame, mask=mask)
                            contours = cv2.findContours(
                            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                            c = max(contours[0], key=cv2.contourArea)
                            minarea = cv2.minAreaRect(c)
                            rect = cv2.boxPoints(minarea)
                            cv2.drawContours(output, [np.int0(rect)], -1, (0, 255, 0), 3)

                        outputKeyed = cv2.subtract(frame, output)


                        gray = cv2.cvtColor(outputKeyed, cv2.COLOR_BGR2GRAY)
                        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,
                           1, 20, param1=50, param2=30, minRadius=8, maxRadius=15)

                        time_e = time.perf_counter()

                        if circles is not None:
                            for n in circles[0]:
                                cv2.circle(gray, (n[0], n[1]), n[2], (255, 0, 0))

                        cv2.imshow('VIDEO', gray)
                        c = cv2.waitKey(1)

                        print(time_e-time_s)

                        if circles is not None:
                            balls = [Ball(1, (i[0], i[1]), BallType.SOLID.name) for i in circles[0]]
                            self.queue.put(balls)
