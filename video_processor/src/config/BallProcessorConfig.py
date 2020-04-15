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
        dp: int,
        minDist: int,
        param1: int,
        param2: int,
    ):
        super(BallProcessorConfig, self).__init__(width, height, afterCutWidth, afterCutHeight)

        self.threshold = threshold
        self.radiusUpper = radiusUpper
        self.radiusLower = radiusLower

        #HoughCircles configs
        self.dp = dp
        self.param1 = param1
        self.param2 = param2
        self.minDist = minDist


