from multiprocessing import Process

class FrameProcessor(Process):
    
    def __init__(self, queue, frame, lock):
        Process.__init__(self)
        self.queue = queue
        self.frameValue = frame
        self.lock = lock

    def run(self):
        pass
