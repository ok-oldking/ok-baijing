# original https://github.com/Toufool/AutoSplit/blob/master/src/capture_method/WindowsGraphicsCaptureMethod.py
import time

import cv2
import numpy as np
from cv2.typing import MatLike
from typing_extensions import override

from autoui.capture.BaseCaptureMethod import BaseCaptureMethod


class ADBCaptureMethod(BaseCaptureMethod):
    name = "ADB command line Capture"
    short_description = "slow but works when in background/minimized, takes 300ms per frame"

    def __init__(self, device):
        super().__init__()
        self.device = device
        frame = self.get_frame()
        self.height, self.width, _ = frame.shape
        print(f"ADBCaptureMethod size: {self.width}x{self.height}")

    @override
    def get_frame(self) -> MatLike | None:
        start = time.time()
        png_bytes = self.device.shell("screencap -p", encoding=None)
        # print(f"screencap: {time.time() - start}")
        image_data = np.frombuffer(png_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
