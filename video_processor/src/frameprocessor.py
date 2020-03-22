from multiprocessing import Process

class FrameProcessor(Process):
    
    def __init__(self, queue, frame, lock):
        super().__init__()
        self.queue = queue
        self.frameValue = frame
        self.lock = lock
        self.width = 1280
        self.height = 720

    def run(self):
        pass
