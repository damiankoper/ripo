import cv2
import numpy as np
import sys
import os
from multiprocessing import Array, Queue, Value, Lock, RawArray
from ballprocessor import BallProcessor
from cueprocessor import CueProcessor
from outputmodule import OutputModule
import ctypes
import cProfile
import time

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

class VideoProcessor:

    def __init__(self):
        self.ballsQueue = Queue()
        self.cueQueue = Queue()

        self.vcap = None

        self.frameReadLock = Lock()

        self.sharedArray = RawArray(np.ctypeslib.as_ctypes_type(np.uint8), 1280*720*3)  
        self.frameValue = np.frombuffer(self.sharedArray, dtype=np.uint8).reshape(1280*720*3)

        self.ballProcess = BallProcessor(self.ballsQueue, self.sharedArray, self.frameReadLock)
        self.cueProcess = CueProcessor(self.cueQueue, self.sharedArray, self.frameReadLock)
        self.outputModuleProcess = OutputModule(self.ballsQueue, self.cueQueue)

        self.ballProcess.start()
        self.cueProcess.start()
        self.outputModuleProcess.start()

    def capture(self, ip, port):

        try:

            self.vcap = cv2.VideoCapture("udp://"+ip+":"+port, cv2.CAP_FFMPEG)
            
            while(1):
                ret, frame = self.vcap.read()
                if frame is not None:

                    with self.frameReadLock:
                        np.copyto(self.frameValue, frame.flatten())
            
        
        except KeyboardInterrupt:
            self.cleanup()
            self.vcap.release()
            sys.exit(0)

    def cleanup(self):
        self.ballProcess.terminate()
        self.ballProcess.join()

        self.cueProcess.terminate()
        self.cueProcess.join()

        self.outputModuleProcess.terminate()
        self.outputModuleProcess.join()



if __name__ == "__main__":
    vp = VideoProcessor()
    vp.capture("0.0.0.0", "8444")
