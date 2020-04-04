from .FrameProcessingConfig import FrameProcessingConfig


class VideoProcessorConfig(FrameProcessingConfig):

    def __init__(
        self,
        width: int,
        height: int,
        initDuration: int = 60
    ):
        super(VideoProcessorConfig, self).__init__(width, height, None, None)
        self.initDuration = initDuration

        self.afterCutWidth = None
        self.afterCutHeight = None
