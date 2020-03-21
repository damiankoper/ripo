from multiprocessing import Process

class OutputModule(Process):
    
    def __init__(self, ballsQueue, cueQueue):
        Process.__init__(self)
        self.ballsQueue = ballsQueue
        self.cueQueue = cueQueue

    def run(self):
        while(1):
            if not self.ballsQueue.empty():
                pass
            if not self.cueQueue.empty():
                pass

                
                    
