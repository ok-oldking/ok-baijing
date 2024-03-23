from abc import abstractmethod

from autohelper.gui.Communicate import communicate
from autohelper.logging.Logger import get_logger


class Scene:
    name = None
    executor = None

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def detect(self, frame):
        return False

    @staticmethod
    def draw_boxes(feature_name, boxes, color="red"):
        communicate.draw_box.emit(feature_name, boxes, color)
