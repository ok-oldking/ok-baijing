from autohelper.capture.adb.ADBCaptureMethod import screencap
from autohelper.interaction.BaseInteraction import BaseInteraction
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class ADBBaseInteraction(BaseInteraction):

    def __init__(self, device, capture):
        super().__init__(capture)
        self.width = 0
        self.height = 0
        self.device = device
        screencap(self)
        logger.info(f"width: {self.width}, height: {self.height}")
        if self.width == 0 or self.height == 0:
            logger.critical(f"Could not parse screen resolution. {result}")
            raise RuntimeError(f"ADBBaseInteraction: Could not parse screen resolution. {result}")

    def send_key(self, key, down_time=0.02):
        super().send_key(key, down_time)
        self.device.shell(f"input keyevent {key}")

    def click(self, x=-1, y=-1):
        super().click(x, y)
        x = int(x * self.width / self.capture.width)
        y = int(y * self.height / self.capture.height)
        self.device.shell(f"input tap {x} {y}")
