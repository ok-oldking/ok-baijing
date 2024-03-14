# original https://github.com/Toufool/AutoSplit/blob/master/src/capture_method/WindowsGraphicsCaptureMethod.py

from cv2.typing import MatLike
from typing_extensions import override

from autohelper.capture.BaseCaptureMethod import BaseCaptureMethod
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class ADBCaptureMethod(BaseCaptureMethod):
    name = "ADB command line Capture"
    description = "use the adb screencap command, slow but works when in background/minimized, takes 300ms per frame"

    def __init__(self, device_manager):
        super().__init__()
        self.device_manager = device_manager
        print(f"ADBCaptureMethod size: {self.width}x{self.height}")

    @property
    def width(self):
        return self.device_manager.width

    @property
    def height(self):
        return self.device_manager.height

    @override
    def get_frame(self) -> MatLike | None:
        return self.device_manager.screencap()
