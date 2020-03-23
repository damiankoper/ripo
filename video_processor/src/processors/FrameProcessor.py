from multiprocessing import Process, Queue, Lock, RawArray

class FrameProcessor(Process):
    
    def __init__(self, queue: Queue, frame: RawArray, lock: Lock, width: int, height: int):
        Process.__init__(self)
        self.queue = queue
        self.frameValue = frame
        self.lock = lock
        self.width = width
        self.height = height

    def run(self):
        pass
