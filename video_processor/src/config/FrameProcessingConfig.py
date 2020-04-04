from multiprocessing import Value
from .GlobalConfig import GlobalConfig


class FrameProcessingConfig(GlobalConfig):

    def __init__(
        self,
        width,
        height,
        afterCutWidth: Value,
        afterCutHeight: Value,
    ):
        super(FrameProcessingConfig, self).__init__(width, height)

        self.afterCutWidth = afterCutWidth
        self.afterCutHeight = afterCutHeight

        self.pool_color_range = [[70, 150, 50], [95, 255, 220]]
