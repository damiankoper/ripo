from frameprocessor import FrameProcessor

class CueProcessor(FrameProcessor):
  
    def run(self):
        while(1):
            if self.frameValue is not None:
                while(1):
                    with self.lock:
                        pass

                    something=1

                    self.queue.put(something)
