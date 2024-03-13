from abc import abstractmethod

from autohelper.feature.FindFeature import FindFeature
from autohelper.scene.Scene import Scene


class FindFeatureScene(Scene, FindFeature):
    def __init__(self):
        Scene.__init__(self)
        self.feature_set = None

    @abstractmethod
    def detect(self, frame):
        return False
