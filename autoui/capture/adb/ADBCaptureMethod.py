# original https://github.com/Toufool/AutoSplit/blob/master/src/capture_method/WindowsGraphicsCaptureMethod.py

import cv2
import numpy as np
from cv2.typing import MatLike
from typing_extensions import override

from autoui.capture.BaseCaptureMethod import BaseCaptureMethod


class ADBCaptureMethod(BaseCaptureMethod):
    name = "ADB command line Capture"
    description = "use the adb screencap command, slow but works when in background/minimized, takes 300ms per frame"

    def __init__(self, device):
        super().__init__()
        self.device = device
        self.get_frame()
        print(f"ADBCaptureMethod size: {self.width}x{self.height}")

    @override
    def get_frame(self) -> MatLike | None:
        return screencap(self)


def screencap(obj_with_device) -> MatLike | None:
    png_bytes = obj_with_device.device.shell("screencap -p", encoding=None)
    image_data = np.frombuffer(png_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    obj_with_device.height, obj_with_device.width, _ = image.shape
    return image
