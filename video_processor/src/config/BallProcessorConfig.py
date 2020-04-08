from .FrameProcessingConfig import FrameProcessingConfig


class BallProcessorConfig(FrameProcessingConfig):
    
    def __init__(
        self,
        width,
        height,
        afterCutWidth,
        afterCutHeight,
        threshold: int,
        radiusLower: int,
        radiusUpper: int,
    ):
        super(BallProcessorConfig, self).__init__(width, height, afterCutWidth, afterCutHeight)

        self.threshold = threshold
        self.radiusUpper = radiusUpper
        self.radiusLower = radiusLower
