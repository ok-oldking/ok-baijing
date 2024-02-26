from abc import abstractmethod

from autoui.feature.FeatureSet import FeatureSet
from autoui.feature.FindFeature import FindFeature
from autoui.scene.Scene import Scene


class FindFeatureScene(Scene, FindFeature):
    def __init__(self, feature_set: FeatureSet):
        Scene.__init__(self)
        self.feature_set = feature_set

    @abstractmethod
    def detect(self, frame):
        return False
