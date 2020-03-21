import cv2
import numpy as np
from frameprocessor import FrameProcessor
from ball import Ball
import numpy as np


class BallProcessor(FrameProcessor):

    def run(self):
        while(1):
            #wiem, że ten if teraz nie działa
            if self.frameValue is not None:
                while(1):
                    with self.lock:
                        frame = np.frombuffer(self.frameValue, dtype=np.uint8)
                        frame = frame.reshape(720, 1280, 3)

                    something = 1

                    self.queue.put(something)
