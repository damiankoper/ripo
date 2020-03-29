from multiprocessing import Value

class GlobalConfig:

    def __init__(self, width: int, height: int):
        
        self.width = width

        self.height = height


    def get_shape(self):
        return self.width*self.height*3


class FrameProcessingConfig(GlobalConfig):

     def __init__(self, width, height, afterCutWidth: Value, afterCutHeight: Value):
        super(FrameProcessingConfig, self).__init__(width, height)

        self.afterCutWidth = afterCutWidth

        self.afterCutHeight = afterCutHeight


