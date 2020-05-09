from .FrameProcessor import FrameProcessor

import cv2
import numpy as np

import time

from ..pool_state.Player import Player, PlayerName
from ..pool_state.Cue import Cue

class CueProcessor(FrameProcessor):
  
    def eventHandling(self):
        while not self.eventQueue.empty():
            self.event = self.eventQueue.get_nowait()

            ####

    def run(self):
        try:
            self._run()
        except(KeyboardInterrupt, SystemExit):
            print("CP: Interrupt")
        print("CP: Exit")


    def _run(self):

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

            difference = cv2.absdiff(frameAvg, frame)

            difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(
                difference, 30, 255, cv2.THRESH_BINARY)

            iterations = 1

            # thresh = cv2.morphologyEx(
            #     thresh, cv2.MORPH_OPEN, open_kernel, iterations=iterations)
            # thresh = cv2.morphologyEx(
            #     thresh, cv2.MORPH_CLOSE, close_kernel, iterations=iterations)


            minLineLength = 100
            maxLineGap = 140
            lines = cv2.HoughLinesP(thresh,1,np.pi/180,200,minLineLength,maxLineGap)

            if lines is not None:            
                for x1,y1,x2,y2 in lines[0]:
                    cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)

                player = Player(PlayerName.A, (0, 255, 0))

                cues = []

                cues.append(Cue(self.normalizeCoordinates((x1, y1)),
                                self.normalizeCoordinates((x2, y2)),
                                player))


                self.queue.put(cues)

            cv2.imshow('CP: DETECTED', frame)



            cv2.waitKey(1)

