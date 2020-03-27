from .FrameProcessor import FrameProcessor

class CueProcessor(FrameProcessor):
  
    def run(self):
        while(1):
            self.throttle.put(1)
            self.throttle.join()
            with self.lock:
                pass

                something=1

                self.queue.put(something)
