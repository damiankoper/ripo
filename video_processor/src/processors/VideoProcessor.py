import argparse
import cProfile
import ctypes
import os
import sys
import time
from multiprocessing import Array, Lock, Queue, RawArray, Value

import cv2
import numpy as np

from .BallProcessor import BallProcessor
from .CueProcessor import CueProcessor
from ..output_module.OutputModule import OutputModule

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

class VideoProcessor:

    def __init__(self):
        self.ballsQueue = Queue()
        self.cueQueue = Queue()

        self.vcap = None
        self.vrec = None

        self.frameReadLock = Lock()

        self.ballProcess = None
        self.cueProcess = None
        self.outputModuleProcess = None
   
    def capture(self, width: int, height: int, port: str):

        sharedArray = RawArray(np.ctypeslib.as_ctypes_type(np.uint8), width*height*3)  
        frameValue = np.frombuffer(sharedArray, dtype=np.uint8).reshape(width*height*3)

        self.ballProcess = BallProcessor(self.ballsQueue, sharedArray, self.frameReadLock, width, height)
        self.cueProcess = CueProcessor(self.cueQueue, sharedArray, self.frameReadLock, width, height)
        self.outputModuleProcess = OutputModule(self.ballsQueue, self.cueQueue, port)

        self.ballProcess.start()
        self.cueProcess.start()
        self.outputModuleProcess.start()

        try:
            self.vcap = cv2.VideoCapture("udp://0.0.0.0:8444", cv2.CAP_FFMPEG)

            while(1):
                ret, frame = self.vcap.read()

                if frame is not None:
                    with self.frameReadLock:
                        np.copyto(frameValue, frame.flatten())
            
        
        except KeyboardInterrupt:
            self.terminate()
            self.cleanup()
            sys.exit(0)
            
    def record(self, width: int, height: int, path: str, fps: int = 30):
        try:
            self.vrec = cv2.VideoWriter(
            path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width, height))

            self.vcap = cv2.VideoCapture("udp://0.0.0.0:8444", cv2.CAP_FFMPEG)

            while(1):
                ret, frame = self.vcap.read()
                if frame is not None:
                    self.vrec.write(frame)
                    cv2.imshow('VIDEO', frame)
                    c = cv2.waitKey(1)
                    if c & 0xFF == ord('q'):
                        self.cleanup()
                        break

        except KeyboardInterrupt:
            self.cleanup()
            sys.exit(0)

    def cleanup(self):
        if self.vrec is not None:
            self.vrec.release()
        if self.vcap is not None:
            self.vcap.release()

    def terminate(self):
        self.ballProcess.terminate()
        self.ballProcess.join()

        self.cueProcess.terminate()
        self.cueProcess.join()

        self.outputModuleProcess.terminate()
        self.outputModuleProcess.join()


'''
if __name__ == "__main__":
    vp = VideoProcessor()

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument("-c", "--capture", help="Main funcionality, captures frames and sends them to other processors")
    group.add_argument("-r", "--record", help="Recording only")
    
    parser.add_argument("-w", "--width", help="Width", required=True, type=int)
    parser.add_argument("-ht", "--height", help="Height", required=True, type=int)
    parser.add_argument("-f", "--fps", help="Used in recording", required=False, type=int)
    args = parser.parse_args()

    if args.capture:
        vp.capture(args.width, args.height, args.capture)

    if args.record:
        if args.fps:
            vp.record(args.width, args.height, args.record, args.fps)
        else:
            vp.record(args.width, args.height, args.record)
'''
