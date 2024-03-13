from abc import abstractmethod


class Scene:
    name = None

    def __init__(self):
        pass

    @abstractmethod
    def detect(self, frame):
        return False
