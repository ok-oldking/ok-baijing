import adbutils
import cv2
import numpy as np

from autohelper.capture.adb.vbox import installed_emulator
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class DeviceManager:

    def __init__(self):
        self._device = None

        self.height = 0
        self.width = 0
        self.installed_emulators = installed_emulator()

        self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        logger.debug(f'connect adb')
        for info in self.adb.list():
            logger.debug(f'adb.list() {info}')

        for emulator in self.installed_emulators:
            self.adb.connect(emulator.adb_address)

        if self.adb.device_list():
            self._device = self.adb.device_list()[0]
        self.screencap()

    @property
    def device(self):
        return self._device

    def update_device_list(self):
        pass

    def shell(self, *args, **kwargs):
        device = self.device
        if device is not None:
            try:
                return device.shell(*args, **kwargs)
            except Exception as e:
                logger.error(f"shell_wrapper error occurred: {e}")

    def screencap(self) -> np.ndarray | None:
        png_bytes = self.shell("screencap -p", encoding=None)
        if png_bytes is not None and len(png_bytes) > 0:
            image_data = np.frombuffer(png_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            if image is not None:
                self.height, self.width, _ = image.shape
                return image
            else:
                logger.error(f"Screencap image decode error, probably disconnected")
