from .FrameProcessor import FrameProcessor

class CueProcessor(FrameProcessor):
  
    def eventHandling(self):
        while not self.eventQueue.empty():
            self.event = self.eventQueue.get_nowait()

            ####

    def run(self):
        while(1):

            self.throttle.put(1)

            self.eventHandling()

            self.throttle.join()

            with self.lock:
                frame = np.frombuffer(self.frameValue, dtype=np.uint8)
                frameAvg = np.frombuffer(self.frameAvgValue, dtype=np.uint8)

                self.width = self.config.afterCutWidth.value
                self.height = self.config.afterCutHeight.value

            frame = np.resize(frame, self.width*self.height*3)
            frame = frame.reshape(self.height, self.width, 3)

            frameAvg = np.resize(frameAvg, self.width*self.height*3)
            frameAvg = frameAvg.reshape(self.height, self.width, 3)

            difference = cv2.absdiff(frameAvg, frame)

            difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(
                difference, 8, 255, cv2.THRESH_BINARY)

            iterations = 1

            thresh = cv2.morphologyEx(
                thresh, cv2.MORPH_OPEN, open_kernel, iterations=iterations)
            thresh = cv2.morphologyEx(
                thresh, cv2.MORPH_CLOSE, close_kernel, iterations=iterations)