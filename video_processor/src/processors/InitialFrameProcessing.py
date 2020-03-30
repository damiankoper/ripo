import cv2
import numpy as np
import ctypes


class InitialFrameProcessing:

    def __init__(self, averaging_time, boundaries):

        # Config
        self.averaging_time = averaging_time
        self.boundaries = boundaries
        self.mask_tredhold = 20

        # Avg frame
        self.avg_frame_buffer = None
        self.avg_frame_samples_count = 0
        self.avg_frame = None

        # Avg calc results
        self.M = None
        self.maxHeight = None
        self.maxWidth = None

        # Live calc results
        self.warped_frame = None
        self.warped_masked_frame = None

    def _calc_avg_frame(self, frame):
        self.avg_frame_samples_count += 1
        self.avg_frame_buffer = frame.astype(
            ctypes.c_uint64) if self.avg_frame_buffer is None else self.avg_frame_buffer+frame
        self.avg_frame = (self.avg_frame_buffer /
                          self.avg_frame_samples_count).astype(ctypes.c_uint8)

    def _calc_avg_components(self, frame):
        imageHSV = cv2.cvtColor(self.avg_frame, cv2.COLOR_BGR2HSV)

        lower = np.array(self.boundaries[0], dtype="uint8")
        upper = np.array(self.boundaries[1], dtype="uint8")

        mask = cv2.inRange(imageHSV, lower, upper)

        #self.output = cv2.bitwise_and(frame, frame, mask=mask)
        contours = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        c = max(contours[0], key=cv2.contourArea)
        minarea = cv2.minAreaRect(c)
        rect = cv2.boxPoints(minarea)

        # It is always a rect since camera is perpendicular to table
        # So we need to calc distance between corners to get w and h
        a = np.linalg.norm(rect[0]-rect[1])
        b = np.linalg.norm(rect[1]-rect[2])

        # Greater is width, lower is height
        self.maxWidth = max(a, b)
        self.maxHeight = min(a, b)

        dest = np.float32([
            [0, self.maxHeight-1],
            [0, 0],
            [self.maxWidth - 1, 0],
            [self.maxWidth - 1, self.maxHeight - 1],
        ])
        self.M = cv2.getPerspectiveTransform(rect, dest)

    def on_frame(self, frame):
        # Avg process
        if self.averaging_time > 0:
            self._calc_avg_frame(frame)
            self._calc_avg_components(frame)
            self.averaging_time -= 1

        # Every frame from here
        self.warped_masked_frame = self._mask(frame)
        self.warped_masked_frame = self._warp(self.warped_masked_frame)
        self.warped_frame = self._warp(frame)

    def _warp(self, frame):
        return cv2.warpPerspective(
            frame, self.M, (self.maxWidth, self.maxHeight))

    def _mask(self, frame):
        frameSubtracted = cv2.cvtColor(cv2.subtract(
            ~frame, ~self.avg_frame) + cv2.subtract(
                frame, self.avg_frame), cv2.COLOR_BGR2GRAY)
        #frameSubtracted = cv2.blur(frameSubtracted, (5,5))
        cv2.imshow('IFP: MASK PRE TRESHOLD', frameSubtracted)
        c = cv2.waitKey(1)
        ret, frameKeyedMask = cv2.threshold(
            frameSubtracted, self.mask_tredhold, 255, cv2.THRESH_BINARY)

        return frameKeyedMask

    def get_warped_frame(self, frame):
        return self.warped_frame

    def get_warped_masked_frame(self):
        return self.warped_masked_frame

    def get_pool_size(self):
        return int(self.maxWidth), int(self.maxHeight)

    def display_components(self, wait=False):
        cv2.imshow('IFP: WARPED MASK', self.warped_masked_frame)
        c = cv2.waitKey(1)
        cv2.imshow('IFP: WARPED FRAME', self.warped_frame)
        c = cv2.waitKey(1)
        cv2.imshow('IFP: AVG FRAME', self.avg_frame)
        c = cv2.waitKey(1 if not wait else 0)
