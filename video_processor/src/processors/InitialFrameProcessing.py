import cv2
import numpy as np
import ctypes
from ..config.VideoProcessorConfig import VideoProcessorConfig


class InitialFrameProcessing:

    def __init__(self, config: VideoProcessorConfig):

        # Config
        self.config = config

        self.reset_avg()

        # Live calc results
        self.warped_frame = None

    def reset_avg(self):
        # Avg frame
        self.averaging_time_left = self.config.initDuration
        self.avg_frame_buffer = None
        self.avg_frame_samples_count = 0
        self.avg_frame = None

        # Avg calc results
        self.warp_matrix = None
        self.warp_height = None
        self.warp_width = None

    def _calc_avg_frame(self, frame):
        self.avg_frame_samples_count += 1
        self.avg_frame_buffer = frame.astype(
            ctypes.c_uint64) if self.avg_frame_buffer is None else self.avg_frame_buffer+frame
        self.avg_frame = (self.avg_frame_buffer /
                          self.avg_frame_samples_count).astype(ctypes.c_uint8)

    def _calc_avg_warp_matrix(self, frame):
        imageHSV = cv2.cvtColor(self.avg_frame, cv2.COLOR_BGR2HSV)

        lower = np.array(self.config.pool_color_range[0], dtype="uint8")
        upper = np.array(self.config.pool_color_range[1], dtype="uint8")

        mask = cv2.inRange(imageHSV, lower, upper)
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
        self.warp_width = max(a, b)
        self.warp_height = min(a, b)

        dest = np.float32([
            [0, self.warp_height-1],
            [0, 0],
            [self.warp_width - 1, 0],
            [self.warp_width - 1, self.warp_height - 1],
        ])
        self.warp_matrix = cv2.getPerspectiveTransform(rect, dest)

    def on_frame(self, frame):
        # Avg process
        if self.averaging_time_left > 0:
            self._calc_avg_frame(frame)
            self._calc_avg_warp_matrix(frame)
            self.avg_frame = self._warp(self.avg_frame)
            self.averaging_time_left -= 1

        self.warped_frame = self._warp(frame)

    def _warp(self, frame):
        return cv2.warpPerspective(
            frame, self.warp_matrix, (self.warp_width, self.warp_height))

    def get_warped_frame(self):
        return self.warped_frame

    def get_avg_frame(self):
        return self.avg_frame

    def get_pool_size(self):
        return int(self.warp_width), int(self.warp_height)

    def display_components(self):
        cv2.imshow('IFP: WARPED FRAME', self.warped_frame)
        cv2.imshow('IFP: AVG FRAME', self.avg_frame)
