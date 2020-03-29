from .FrameProcessor import FrameProcessor

class CueProcessor(FrameProcessor):
  
    def eventHandling(self):
        while not self.eventQueue.empty():
            self.event = self.eventQueue.get_nowait()

            ####

    def run(self):
        while(1):
            self.throttle.put(1)
            self.throttle.join()
            with self.lock:
                pass

                something=1

                self.queue.put(something)
