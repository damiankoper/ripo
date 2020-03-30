from .GlobalConfig import GlobalConfig


class VideoConfig(GlobalConfig):

    def __init__(self, width: int, height: int, webPort: int = 8888, udpPort: int = 8444, 
    recordingPath: str = None, recordingFps: int = 30, initTime: int = 60):
        super(VideoConfig, self).__init__(width, height)

        self.webPort = webPort

        self.udpPort = udpPort

        self.recordingPath = recordingPath

        self.recordingFps = recordingFps

        self.initTime = initTime

        self.boundaries = [[70, 150, 50], [95, 255, 220]]

