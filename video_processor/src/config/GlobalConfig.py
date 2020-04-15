

class GlobalConfig:

    def __init__(
        self,
        width: int,
        height: int,
        webPort: int = 8888,
        udpPort: int = 8444,
        recordingPath: str = None,
        recordingFps: int = 30
    ):
        self.width = width
        self.height = height

        self.webPort = webPort
        self.udpPort = udpPort
        
        self.recordingPath = recordingPath
        self.recordingFps = recordingFps

        self.genDataSet = False
        self.genDataSetFolder = None
        
    def get_flat_shape(self):
        return self.width*self.height*3
