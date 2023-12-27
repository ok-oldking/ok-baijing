from abc import abstractmethod

from autoui.feature.FeatureInteraction import FeatureInteraction
from autoui.feature.FeatureSet import FeatureSet
from autoui.scene.Scene import Scene


class FeatureScene(Scene, FeatureInteraction):
    def __init__(self, interaction, feature_set: FeatureSet):
        FeatureInteraction.__init__(self, interaction, feature_set)
        Scene.__init__(self)

    @abstractmethod
    def detect(self, frame):
        return False
