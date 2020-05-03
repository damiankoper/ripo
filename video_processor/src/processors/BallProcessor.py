import time
from enum import Enum

import cv2
import numpy as np
import math
from .FrameProcessor import FrameProcessor
from .Classification import Classification

from ..pool_state.Ball import Ball, BallType
from ..pool_state.Vector2i import Vector2i

from ..events.BallThresholdChangeEvent import BallThresholdChangeEvent
from ..events.BallLowerRadiusChangeEvent import BallLowerRadiusChangeEvent
from ..events.BallUpperRadiusChangeEvent import BallUpperRadiusChangeEvent
from ..events.BalldpChangeEvent import BalldpChangeEvent
from ..events.BallMinDistChangeEvent import BallMinDistChangeEvent
from ..events.BallParam1ChangeEvent import BallParam1ChangeEvent
from ..events.BallParam2ChangeEvent import BallParam2ChangeEvent


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
            elif isinstance(event, BalldpChangeEvent):
                self.config.dp = int(event.dp)
            elif isinstance(event, BallMinDistChangeEvent):
                self.config.minDist = int(event.minDist)
            elif isinstance(event, BallParam1ChangeEvent):
                self.config.param1 = float(event.param1)
            elif isinstance(event, BallParam2ChangeEvent):
                self.config.param2 = float(event.param2)

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

        cropImgN = 0
        cropImgDelay = 0.1

        cropDelayStart = time.perf_counter()

        classificator = Classification()

        classificator.loadModel("data/training/trained_model")

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

            #frameAvg = cv2.GaussianBlur(frameAvg, (5, 5), 0)
            #frameAvg = cv2.filter2D(frameAvg, -1, sharp_kernel)

            #frame = cv2.GaussianBlur(frame, (5, 5), 0)
            #frame = cv2.filter2D(frame, -1, sharp_kernel)

            # To zbyt małą różnice powoduje zbyt dużym kosztem
            # w porównaniu do samej różnicy, trace tutaj aż 0,01s.

            # difference = cv2.add(cv2.absdiff(frameAvg, frame),
            #                       cv2.absdiff(~frameAvg, ~frame))

            difference = cv2.absdiff(frameAvg, frame)

            difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(
                difference, 8, 255, cv2.THRESH_BINARY)

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
                if area > circleArea*0.5 and r < 24 and r > 14:
                    # cv2.circle(frame, (int(x), int(y)), int(20), (0, 255, 255), 2)
                    # cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    circles.append((int(x), int(y)))
                    cv2.drawContours(thresh, [c], 0, (0, 0, 0), -1)
                    count += 1

            masked = cv2.bitwise_and(difference, thresh)

            circles2 = cv2.HoughCircles(image=masked,
                                        method=cv2.HOUGH_GRADIENT,
                                        dp=self.config.dp,
                                        minDist=self.config.minDist,
                                        param1=self.config.param1,
                                        param2=self.config.param2,
                                        minRadius=self.config.radiusLower,
                                        maxRadius=self.config.radiusUpper
                                        )
            circles2filtered = []
            if circles2 is not None:
                circlesRound = np.round(circles2[0, :]).astype("int")
                for (x, y, r) in circlesRound:
                    detectedBefore = False
                    for (cX, cY) in circles:
                        distance = math.sqrt((x-cX)**2 + (y-cY)**2)
                        if distance < self.config.radiusLower*2:
                            detectedBefore = True
                            break
                    if not detectedBefore:
                        circles2filtered.append((int(x), int(y)))
                    # cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    # cv2.circle(frame, (x, y), 20, (0, 255, 255), 2)
            circles = circles+circles2filtered

            if time.perf_counter()-cropDelayStart > cropImgDelay:
                if self.config.genDataSet:
                    if circles is not None:
                        for n in circles:
                            cropImg = frame[int((n[1]-25)):int((n[1]+25)),
                                            int((n[0]-25)):int((n[0]+25))]
                            if cropImg.shape == (50, 50, 3):
                                cv2.imwrite(self.config.genDataSetFolder +
                                            "/data_item"+str(cropImgN)+".png", cropImg)
                                cropImgN += 1
                        cropDelayStart = time.perf_counter()

            timeMS = time.time_ns() // 1000000

            balls = []
            if circles is not None:
                for n in circles:
                    cropImg = frame[int((n[1]-25)):int((n[1]+25)),
                                    int((n[0]-25)):int((n[0]+25))]

                    ball_number = 17
                    if cropImg.shape == (50, 50, 3):
                        ball_number, _ = classificator.classify(cropImg)

                    if ball_number != 'NaB' and ball_number != 17:
                        if int(ball_number) <= 8:
                            ball_type = BallType.SOLID
                        else:
                            ball_type = BallType.STRIPED
                        if int(ball_number) == 16:
                            ball_type = BallType.SOLID

                        balls.append(Ball(int(ball_number), self.normalizeCoordinates(
                            (n[0], n[1])), ball_type, timeMS - (timeMS//1000000*1000000)))

                self.queue.put(balls)

                for ball in balls:
                    cv2.putText(frame, str(ball.number), (int(ball.position.x*self.width), int(ball.position.y*self.height)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)

            cv2.imshow('BP: DETECTED', frame)
            # cv2.imshow('BP: DIFF', difference)
            # cv2.imshow('BP: MASKED', masked)
            #cv2.imshow('BP: THRESH BEFORE', threshBefore)
            #cv2.imshow('BP: AVG FRAME', frameAvg)

            cv2.waitKey(1)
