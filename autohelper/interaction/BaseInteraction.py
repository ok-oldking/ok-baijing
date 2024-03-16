from autohelper.feature.Box import Box
from autohelper.gui.Communicate import communicate
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class BaseInteraction:

    def __init__(self, capture):
        self.capture = capture

    def send_key(self, key, down_time=0.02):
        pass

    def move(self, x, y):
        pass

    def click_relative(self, x, y):
        self.click(int(self.capture.width * x), int(self.capture.height * y))

    def move_relative(self, x, y):
        self.move(int(self.capture.width * x), int(self.capture.height * y))

    def click_box(self, box: Box, relative_x=0.5, relative_y=0.5):
        logger.info(f"click_box {box}")
        communicate.draw_box.emit("click", [box])
        x, y = box.relative_with_variance(relative_x, relative_y)
        self.click(x, y)

    def click(self, x=-1, y=-1):
        logger.info(f"click {x, y}")
        pass
