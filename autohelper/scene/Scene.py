from abc import abstractmethod

from autohelper.gui.Communicate import communicate


class Scene:
    name = None
    executor = None

    def __init__(self):
        pass

    @abstractmethod
    def detect(self, frame):
        return False

    @staticmethod
    def draw_boxes(feature_name, boxes, color="red"):
        communicate.draw_box.emit(feature_name, boxes, color)
