from multiprocessing import Process, Queue, Lock, RawArray, JoinableQueue

class FrameProcessor(Process):
    
    def __init__(self, queue: Queue, throttle: JoinableQueue, frame: RawArray, lock: Lock, width: int, height: int):
        Process.__init__(self)
        self.queue = queue
        self.frameValue = frame
        self.lock = lock
        self.width = width
        self.height = height
        self.throttle = throttle

    def run(self):
        pass
