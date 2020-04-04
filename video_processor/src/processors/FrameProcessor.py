from multiprocessing import Process, Queue, Lock, RawArray, JoinableQueue, Value
from ..config.FrameProcessingConfig import FrameProcessingConfig
from ..pool_state.Vector2i import Vector2i


class FrameProcessor(Process):

    def __init__(
        self,
        queue: Queue,
        throttle: JoinableQueue,
        frame: RawArray,
        avgFrame: RawArray,
        lock: Lock,
        config: FrameProcessingConfig,
        eventQueue: Queue()
    ):
        Process.__init__(self)
        self.queue = queue
        self.frameValue = frame
        self.frameAvgValue = avgFrame
        self.lock = lock
        self.throttle = throttle
        self.config = config
        self.eventQueue = eventQueue

        self.width = None
        self.height = None

    def normalizeCoordinates(self, coordinates: (int, int)):
        return Vector2i(coordinates[0]/self.width, coordinates[1]/self.height)

    def run(self):
        pass
