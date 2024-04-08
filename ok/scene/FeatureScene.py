from abc import abstractmethod

from ok.feature.FindFeature import FindFeature
from ok.scene.Scene import Scene


class FindFeatureScene(Scene, FindFeature):
    def __init__(self):
        Scene.__init__(self)
        self.feature_set = None

    @abstractmethod
    def detect(self, frame):
        return False
