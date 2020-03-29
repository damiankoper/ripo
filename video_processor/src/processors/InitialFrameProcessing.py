import cv2
import numpy as np

class InitialFrameProcessing:
    
    def __init__(self, averaging_time, boundaries):

        self.averaging_time = averaging_time

        self.output = None

        self.M = None

        self.rect = None

        self.boundaries = boundaries

        self.maxHeight = None
        self.maxWidth = None

    def cut(self, frame):
        
        if self.averaging_time > 0:

            imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
            lower = np.array(self.boundaries[0], dtype="uint8")
            upper = np.array(self.boundaries[1], dtype="uint8")

            mask = cv2.inRange(imageHSV, lower, upper)

            self.output = cv2.bitwise_and(frame, frame, mask=mask)
            contours = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            c = max(contours[0], key=cv2.contourArea)
            minarea = cv2.minAreaRect(c)
            rect = cv2.boxPoints(minarea)
     
            if self.rect is not None:
                self.rect = (self.rect + rect) * 0.5
            else:
                self.rect = rect

            width = self.rect[2][0] - self.rect[0][0]
            height = self.rect[0][1] - self.rect[2][1]

            width2 = self.rect[3][0] - self.rect[1][0]
            height2 = self.rect[3][1] - self.rect[2][1]

            self.maxWidth = max(width, width2)
            self.maxHeight = max(height, height2)

            dest = np.float32([
            [0, self.maxHeight-1],
            [0, 0],
            [self.maxWidth - 1, 0],
            [self.maxWidth - 1, self.maxHeight - 1],
            ])

            self.M = cv2.getPerspectiveTransform(self.rect, dest)

            #self.averaging_time -= 1

        outputKeyed = cv2.subtract(frame, self.output)
        warp = cv2.warpPerspective(outputKeyed, self.M, (self.maxWidth, self.maxHeight))

        return warp, int(self.maxWidth), int(self.maxHeight)



